#!/usr/bin/env python3
"""Last gate before push: scan every HTML file the live site will serve.
Exit 1 = do not push. Run from anywhere; it locates the repo root itself."""
import os, re, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'mcb-astro', 'node_modules', 'tools', '_cdn_dl', '_cdn_dl2', '.vercel'}
# Homeowner-education guides that tell people to verify ANY contractor's registration.
# They make no claim about MCB. Doug decides whether they stay; they do not block a deploy.
ADVISORY = {'blog/how-to-choose-general-contractor-massachusetts', 'how-to-hire-contractor-massachusetts'}
CLAIM = re.compile(r"\b(licen[cs]ed|insured|bonded|carries insurance)\b|\b(HIC|CSL)\b|Construction Supervisor|Home Improvement Contractor|workers.{0,8}comp", re.I)
fails, warns, n = [], [], 0
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    for fn in fns:
        if not fn.endswith('.html'): continue
        p = os.path.join(dp, fn); n += 1
        url = os.path.relpath(dp, ROOT).replace('\\', '/')
        h = open(p, encoding='utf8', errors='replace').read()
        hits = [h[max(0, m.start()-40):m.end()+40].replace('\n', ' ') for m in CLAIM.finditer(h)]
        if hits: (warns if url in ADVISORY else fails).append((url, len(hits), hits[0]))
        if 'NM846W2P' in h: fails.append((url, 1, 'tag id NM846W2P still present (GA4 must be G-7HXJQJL5Q2 only)'))
        if 'insertBefore(t,s)}(window' in h.replace(' ', ''): fails.append((url, 1, 'Meta pixel loads itself before consent'))
        if "'mcb_consent'" in h: fails.append((url, 1, 'wrong consent key mcb_consent (static site uses mcb-consent)'))
        for b in re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', h, re.S):
            try: json.loads(b)
            except Exception as e: fails.append((url, 1, 'JSON-LD does not parse: ' + str(e)[:60]))
home = open(os.path.join(ROOT, 'index.html'), encoding='utf8').read()
if '1171 Main' not in home: fails.append(('/', 1, 'street address missing from homepage'))

# ---- sitemap <-> canonical consistency (added 2026-09-18) ----
# Every URL in sitemap.xml must serve a page whose canonical is itself. A page that
# canonicalises elsewhere (the kitchen/bathroom town pages -> their GC page) must not
# be listed. FAIL for pages published by publish_astro.py (the manifest), note-only
# for the older static pages until one clean run has been read.
try:
    manifest = set(json.load(open(os.path.join(ROOT, 'mcb-astro', 'published-manifest.json')))['files'])
except Exception:
    manifest = set()
sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf8').read()
locs = re.findall(r'<loc>https://mcitybuilders\.com([^<]*)</loc>', sm)
sm_mismatch = 0
for loc in locs:
    path = loc.rstrip('/')
    rel = (path.lstrip('/') + '/index.html') if path else 'index.html'
    fp = os.path.join(ROOT, *rel.split('/'))
    if not os.path.exists(fp):
        (fails if rel in manifest else warns).append((path or '/', 1, 'in sitemap but no index.html on disk')); continue
    c = re.search(r'<link rel="canonical" href="([^"]+)"', open(fp, encoding='utf8', errors='replace').read())
    canon = (c.group(1).replace('https://mcitybuilders.com', '').rstrip('/')) if c else None
    if canon != path:
        sm_mismatch += 1
        (fails if rel in manifest else warns).append((path or '/', 1, f'in sitemap but canonical is {c.group(1) if c else "MISSING"}'))
print(f'site_gate: sitemap {len(locs)} URLs, {sm_mismatch} with a canonical that is not itself')
print(f'site_gate: scanned {n} HTML files')
for u, c, s in warns:
    if u in ADVISORY: print(f'  note  /{u}: {c} advisory mention(s) (homeowner guide, not an MCB claim)')
    else: print(f'  note  {u}: {s}')
for u, c, s in fails: print(f'  FAIL  {u if u.startswith("/") else "/" + u}: {c} hit(s) e.g. "...{s}..."')
if fails: sys.exit(f'site_gate: {len(fails)} FAILURE(S). Do not push.')
print('site_gate: PASS')
