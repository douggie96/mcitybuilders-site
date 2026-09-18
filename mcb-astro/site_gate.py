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
print(f'site_gate: scanned {n} HTML files')
for u, c, s in warns: print(f'  note  /{u}: {c} advisory mention(s) (homeowner guide, not an MCB claim)')
for u, c, s in fails: print(f'  FAIL  /{u}: {c} hit(s) e.g. "...{s}..."')
if fails: sys.exit(f'site_gate: {len(fails)} FAILURE(S). Do not push.')
print('site_gate: PASS')
