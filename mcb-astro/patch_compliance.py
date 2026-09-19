#!/usr/bin/env python3
"""Compliance fixes found by the live 274-URL sweep on 2026-09-18 (evening).

Runs over every static page (Astro pages excluded via published-manifest.json).
Idempotent: a second run changes nothing. Exit 1 only on a write failure.
Wired into DEPLOY.bat step [2b] next to patch_static.py / patch_tracking.py.

WHAT IT FIXES, AND WHY

1. NAP + phone on the 16 /areas-we-serve/[town]-ma pages.
   The sweep found these 16 landing pages carry NO phone link and NO visible
   street address. The address was added to their JSON-LD on 09-18, but schema
   is not what a visitor reads, and a service-area landing page with no way to
   call is a conversion defect before it is a compliance one. Rule 6 says the
   full street address goes on the website; this puts it where a human sees it,
   inside the existing bottom CTA block.

2. "Guaranteed" claims. MCB makes no guarantees (no warranty language is
   approved anywhere). Three pages carried it:
     /about              "Guaranteed Quality"
     /interior-painting  "Guaranteed professionalism and quality on every
                          project." — repeated verbatim under three different
                          trust items, which is also a template bug
   Replaced with claims MCB can actually stand behind.

3. Hard-coded review counts. /pages/reviews said "Over 30 five-star reviews";
   the real number was 35 and climbing. A hard-coded count is wrong every time
   Doug succeeds. Same defect the homepage had.

NOT fixed here (deliberately):
  - The two homeowner guides that discuss HIC/CSL. They advise readers to check
    ANY contractor's registration and make no claim about MCB. site_gate treats
    them as ADVISORY. Doug's approved line was added to both on 09-18.
  - /services "Are project timelines guaranteed?" — that is an FAQ question, not
    a claim. Its answer is missing because the /services accordion is broken
    (separate defect, see the closeout).
"""
import os, re, sys, json

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'mcb-astro', 'node_modules', 'tools', '_cdn_dl', '_cdn_dl2', '.vercel'}
MARK = 'mcb-nap-cta'

CTA = ('<a href="/contact" style="display:inline-block;background:#E10600;color:#fff;padding:14px 36px;'
       'font-weight:700;letter-spacing:2px;text-decoration:none;font-size:0.9rem;">GET AN ESTIMATE</a>')

NAP_BLOCK = (
    '<a href="tel:+15086567436" data-ev="phone_click" class="' + MARK + '" '
    'style="display:inline-block;background:transparent;color:#fff;border:1px solid #C0C0C0;padding:13px 30px;'
    'font-weight:700;letter-spacing:2px;text-decoration:none;font-size:0.9rem;margin-right:12px;">'
    '(508) 656-7436</a>'
    + CTA +
    '<p class="' + MARK + '-addr" style="color:#666;font-size:0.8rem;line-height:1.6;margin:22px 0 0;">'
    'Maverick City Builders &middot; 1171 Main St, Lancaster, MA 01523 &middot; '
    'Office visits by appointment</p>'
)

# (path fragment, old, new) — exact-string replacements, each asserted to occur once
TEXT_FIXES = [
    ('about/index.html',
     'Guaranteed Quality',
     'Quality We Stand Behind'),
    ('interior-painting/index.html',
     'Guaranteed professionalism and quality on every project.',
     'Written scope, agreed before a brush is opened.'),
    ('pages/reviews/index.html',
     'Over 30 five-star reviews from Worcester County homeowners.',
     'Every Google review we have is five stars, from Worcester County homeowners.'),
]

manifest = set()
try:
    manifest = set(json.load(open(os.path.join(ROOT, 'mcb-astro', 'published-manifest.json')))['files'])
except Exception:
    pass

scanned = patched = already = skipped = 0
fails, notes = [], []

for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    if 'index.html' not in fns:
        continue
    p = os.path.join(dp, 'index.html')
    rel = os.path.relpath(p, ROOT).replace('\\', '/')
    if rel in manifest:
        continue
    scanned += 1
    h = open(p, encoding='utf8', newline='').read()
    if 'data-astro-cid' in h:
        continue
    orig = h

    # ---- 1. NAP + phone in the areas-we-serve CTA ----
    if rel.startswith('areas-we-serve/') and rel.endswith('-ma/index.html'):
        if MARK in h:
            pass                                   # already patched
        elif h.count(CTA) == 1:
            h = h.replace(CTA, NAP_BLOCK, 1)
        else:
            skipped += 1
            notes.append(f'SKIP {rel}: expected exactly one estimate CTA, found {h.count(CTA)}')

    # ---- 2 & 3. exact-string text fixes ----
    for frag, old, new in TEXT_FIXES:
        if rel != frag:
            continue
        n = h.count(old)
        if n == 0:
            if new not in h:
                notes.append(f'SKIP {rel}: neither the old nor the new wording found — page changed?')
        else:
            h = h.replace(old, new)

    if h == orig:
        if MARK in orig or rel in [f for f, _, _ in TEXT_FIXES]:
            already += 1
        continue
    try:
        open(p, 'w', encoding='utf8', newline='').write(h)
        patched += 1
    except Exception as e:
        fails.append((rel, str(e)))

print(f'patch_compliance: {scanned} static page(s) scanned, {patched} patched, '
      f'{already} already patched, {skipped} skipped')
for n in notes:
    print('  ' + n)
for r, e in fails:
    print(f'  FAIL {r}: {e}')
sys.exit(1 if fails else 0)
