#!/usr/bin/env python3
"""One-shot, idempotent tracking repair for the static pages. Run by DEPLOY.bat.
1. Meta pixel: the inline bootstrap injected fbevents.js itself, so the pixel fired
   BEFORE consent on every page that had it, while the banner says "They load only
   if you accept". Remove the self-injection; the consent-gated loader does the loading.
2. Add that gated loader on pages that had the pixel but no loader.
3. GA4 on G-7HXJQJL5Q2 only: drop the GT-NM846W2P config and loader id.
Skips Astro-published pages (they have their own consent boot in Base.astro)."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'.git', 'mcb-astro', 'node_modules', 'tools', '_cdn_dl', '_cdn_dl2', '.vercel', '_astro'}
G = '<script type="text/plain" data-mcb-src="https://www.googletagmanager.com/gtag/js?id=G-7HXJQJL5Q2"></script>'
F = '<script type="text/plain" data-mcb-src="https://connect.facebook.net/en_US/fbevents.js"></script>'
changed, problems = 0, []
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP]
    for fn in fns:
        if not fn.endswith('.html'): continue
        p = os.path.join(dp, fn)
        o = h = open(p, encoding='utf8', newline='').read()
        if 'data-astro-cid' in h: continue
        h = re.sub(r"n\.queue=\[\];t=b\.createElement\(e\);t\.async=!0;\s*t\.src=v;s=b\.getElementsByTagName\(e\)\[0\];\s*s\.parentNode\.insertBefore\(t,s\)\}", "n.queue=[]}", h)
        h = h.replace('gtag/js?id=GT-NM846W2P', 'gtag/js?id=G-7HXJQJL5Q2')
        h = re.sub(r"""\s*gtag\(["']config["'],\s*["']GT-NM846W2P["']\);""", "", h)
        if 'fbq(' in h and F not in h:
            if h.count(G) == 1: h = h.replace(G, F + G)
            else: problems.append(os.path.relpath(p, ROOT) + ': pixel present but no single GA loader to anchor on')
        if 'NM846W2P' in h: problems.append(os.path.relpath(p, ROOT) + ': NM846W2P still present')
        if 'insertBefore(t,s)}(window' in h.replace(' ', ''): problems.append(os.path.relpath(p, ROOT) + ': pixel still self-injects')
        if h != o:
            open(p, 'w', encoding='utf8', newline='').write(h); changed += 1
print(f'patch_tracking: {changed} file(s) changed')
for x in problems: print('  FAIL', x)
sys.exit(1 if problems else 0)
