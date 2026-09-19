#!/usr/bin/env python3
"""Deploy-2 (2026-09-18, Doug's decision): GA4 loads by default in Consent Mode
"denied" (cookieless pings, no _ga cookie), upgrades to "granted" on Accept.
The Meta pixel stays gated behind Accept. Do-Not-Track / Global Privacy Control
browsers get nothing at all, which keeps the Cookie Policy's DNT promise true.

Runs on every static index.html (not the Astro pages, which get the same
behaviour from Base.astro). Idempotent: a second run changes nothing.
Run by DEPLOY.bat step [2b]. Exit 1 only if a write fails.
"""
import os, re, sys, json

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'mcb-astro', 'node_modules', 'tools', '_cdn_dl', '_cdn_dl2', '.vercel'}
GA = 'https://www.googletagmanager.com/gtag/js?id=G-7HXJQJL5Q2'
MARK = '/* mcb-consent-v2 */'

# 1. gtag.js loads immediately (consent already defaulted to denied two lines
#    above this in every static page) unless the browser asks not to be tracked.
LOADER = ("\n" + MARK + "(function(){try{if(navigator.doNotTrack=='1'||window.doNotTrack=='1'||navigator.globalPrivacyControl)return;"
          "var s=document.createElement('script');s.async=true;s.src='" + GA + "';document.head.appendChild(s);}catch(e){}})();\n")
DEFAULT_RE = re.compile(r"(gtag\('consent','default',\{[^}]*\}\);)")

# 2. load() must not add gtag.js a second time on Accept.
OLD_LOAD = "var n=document.createElement('script'); n.async=true; n.src=s.getAttribute('data-mcb-src');"
NEW_LOAD = ("var u=s.getAttribute('data-mcb-src'); if(document.querySelector('script[src=\"'+u+'\"]'))return;"
            " var n=document.createElement('script'); n.async=true; n.src=u;")

# 3. Banner copy must describe what actually happens.
OLD_BANNER = re.compile(r"We use analytics cookies to understand how the site is used\.\s+They load only if you accept\.")
NEW_BANNER = ("We measure page views with Google Analytics in cookieless mode. Accept to allow analytics cookies and ad measurement; "
              "Decline to stay cookieless.")

scanned = patched = already = skipped = 0
fails = []
manifest = set()
try:
    manifest = set(json.load(open(os.path.join(ROOT, 'mcb-astro', 'published-manifest.json')))['files'])
except Exception:
    pass

for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    if 'index.html' not in fns: continue
    p = os.path.join(dp, 'index.html')
    rel = os.path.relpath(p, ROOT).replace('\\', '/')
    if rel in manifest: continue          # Astro page: Base.astro handles it
    scanned += 1
    h = open(p, encoding='utf8', newline='').read()
    if 'data-astro-cid' in h: continue
    if "gtag('consent','default'" not in h or GA not in h:
        skipped += 1; print(f'  SKIP {rel}: no consent bootstrap / GA loader on this page'); continue
    if MARK in h and OLD_LOAD not in h and not OLD_BANNER.search(h):
        already += 1; continue
    new = h
    if MARK not in new:
        new, n = DEFAULT_RE.subn(lambda m: m.group(1) + LOADER, new, count=1)
        if n != 1:
            skipped += 1; print(f'  SKIP {rel}: consent default call not found in the expected shape'); continue
    if OLD_LOAD in new:
        new = new.replace(OLD_LOAD, NEW_LOAD)
    new, nb = OLD_BANNER.subn(NEW_BANNER, new)
    if new == h:
        already += 1; continue
    try:
        open(p, 'w', encoding='utf8', newline='').write(new); patched += 1
    except Exception as e:
        fails.append((rel, str(e)))

print(f'patch_consent: {scanned} static page(s) scanned, {patched} patched, {already} already patched, {skipped} skipped')
for r, e in fails: print(f'  FAIL {r}: {e}')
sys.exit(1 if fails else 0)
