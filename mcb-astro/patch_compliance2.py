#!/usr/bin/env python3
"""Compliance fixes found by the live 273-URL sweep on 2026-09-19, AFTER deploy 1.

Every defect below was measured on the LIVE site at commit 5072b4d and then
re-confirmed against the file on disk. Nothing here is inferred from a label.

Idempotent: a second run changes nothing and prints "already patched".
Never forces: a count that does not match is reported as SKIP and left alone.
Wired into DEPLOY.bat step [2b] after patch_compliance.py.

WHY EACH ONE IS HERE
--------------------

1. "Guaranteed professionalism and quality on every project."
   patch_compliance.py removed this from /interior-painting on 09-18. The
   09-19 sweep found the SAME string live on five more pages, three times each:
   /kitchen-remodeling /bathroom-remodeling /deck-building /exterior-painting
   /general-renovations. The 09-18 fix was scoped to the one page I had grepped
   instead of to the whole site — the proxy error, again.
   MCB guarantees nothing in writing, so the word cannot stay. The three
   occurrences per page also sat under three DIFFERENT trust items with the
   same subtitle, which is a template bug; each slot now gets its own true line.

2. "Certified Waterproofing Experts" (/bathroom-remodeling)
   A certification claim with no certifying body named. Rule 4.2 permits one
   credential claim and this is not it.

3. "MCB is a certified RRP firm" (/interior-painting, x3 incl. FAQ schema) and
   "Maverick City Builders is EPA RRP-certified" (/bathroom-remodeling-fitchburg-ma,
   x2 incl. FAQ schema).
   The problem was never whether MCB works lead-safe — Doug confirmed on 09-19 that
   MCB does hold the Massachusetts credential. The problem is that the claim named
   the WRONG programme. MCB's own pages (/house-painters-worcester-ma,
   /house-painters-clinton-ma, /interior-painting-cost-massachusetts,
   /exterior-painting-cost-massachusetts) correctly explain that Massachusetts is
   one of fifteen jurisdictions running its own authorised programme and that EPA
   certification does not apply here. The site was citing a credential its own
   content says is irrelevant in this state — which is worse than saying nothing,
   because the one homeowner who checks finds the contradiction.
   Now states compliance with the Massachusetts rules plus the approved
   "Certificate on request" formula. No registration number, per Rule 6.
   DOUG APPROVED 2026-09-19 ("yes lead certificate"): the credential is now named
   outright — "Lead-Safe Renovation Contractor license from the Massachusetts
   Department of Labor Standards under 454 CMR 22.00". No registration number,
   per Rule 6. site_gate.py carries this as an explicit approved exception, and
   its CLAIM regex was tightened at the same time so that nothing ELSE can make
   a license claim without failing the deploy.

4. "&amp;#x27;" (/general-contractor-sterling-ma, /general-contractor-clinton-ma)
   Double-escaped apostrophe: readers see a literal &#x27; in the FAQ answer.
   The 09-18 audit recorded ONE page. The sweep found TWO. Recount, always.

5. "Are you ?" (/carpentry, visible h3 + FAQPage schema)
   An earlier `licens` strip removed the words and left a broken question. The
   existing answer is about written contracts and fixed price, so the question
   is restored to the one that answer actually answers.

NOT fixed here, deliberately — these are Doug's calls, not mine:
  - "Maverick City Builders has been in business since 2020" (/general-contractor-
    clinton-ma) and "has been operating since 2020" (/general-contractor-sterling-ma).
    KEPT. Doug confirmed 09-19 that MCB opened in 2020. Rule 4.2's ban on
    years-in-business exists to stop INVENTED experience; a true, checkable
    founding date is not that, and `foundingDate: 2020` in the Lancaster schema
    stays for the same reason. Both decided together, as they should be.
  - The HIC/CSL homeowner guides. They advise readers to check ANY contractor
    and make no claim about MCB. Verified in the 09-19 sweep.
"""
import os, re, sys, json

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'mcb-astro', 'node_modules', 'tools', '_cdn_dl', '_cdn_dl2', '.vercel'}

GUARANTEED = 'Guaranteed professionalism and quality on every project.'
GUARANTEED_PAGES = {
    'kitchen-remodeling/index.html', 'bathroom-remodeling/index.html',
    'deck-building/index.html', 'exterior-painting/index.html',
    'general-renovations/index.html',
}
# one line per trust slot, in document order — all three are statements of
# process, none is a guarantee, a credential or a count
GUARANTEED_NEW = [
    'Written scope and a fixed price, agreed before work starts.',
    'One point of contact from the estimate through the final walkthrough.',
    'Anything we find gets priced in writing before the work continues.',
]

# (rel path or None for every page, old, new, expected occurrences)
FIXES = [
    ('bathroom-remodeling/index.html',
     'Certified Waterproofing Experts',
     'Waterproofing Detailed to Spec', 1),

    ('bathroom-remodeling-fitchburg-ma/index.html',
     'we follow RRP containment and disposal protocols',
     'we follow the required containment and disposal protocols', 2),

    # Doug confirmed 2026-09-19 that MCB carries a one-year warranty. "one written
    # warranty" was vague enough to read as an open-ended promise; this states the term.
    ('carpentry/index.html',
     'one point of contact and one written warranty.',
     'one point of contact and one written one-year warranty.', 2),

    ('general-contractor-sterling-ma/index.html', '&amp;#x27;', '&#x27;', 1),
    ('general-contractor-clinton-ma/index.html',  '&amp;#x27;', '&#x27;', 1),

    ('carpentry/index.html', 'Are you ?', 'Do you work to a written contract?', 2),
]

# Each entry is (rel, [any of these old strings], the one new string, occurrences).
# A CHAIN entry exists because this copy has been edited more than once: a pristine
# checkout still carries the original wording, while the live file carries the
# intermediate wording from the 09-19 14:00 deploy. Both must converge on the same
# final text, or a fresh clone and Doug's machine drift apart.
LEAD_SAFE_LONG = (
    'We hold a Lead-Safe Renovation Contractor license from the Massachusetts Department of '
    'Labor Standards under 454 CMR 22.00 \u2014 the program that applies here, not the federal '
    'one. On pre-1978 homes that means containment, HEPA vacuuming, and proper disposal. '
    'Certificate on request.'
)
CHAIN = [
    ('interior-painting/index.html',
     ['MCB is a certified RRP firm, and we run those steps',
      'We work to the Massachusetts lead-safe renovation rules, and we run those steps'],
     'We hold a Lead-Safe Renovation Contractor license from the Massachusetts Department of '
     'Labor Standards, and we run those steps', 1),
    ('interior-painting/index.html',
     ['MCB is a certified RRP firm and follows proper containment, HEPA vacuuming, and disposal.',
      'We work to the Massachusetts lead-safe renovation rules on pre-1978 homes: containment, '
      'HEPA vacuuming, and proper disposal. Certificate on request.'],
     LEAD_SAFE_LONG, 2),
    ('bathroom-remodeling-fitchburg-ma/index.html',
     ['Yes. Maverick City Builders is EPA RRP-certified for work in pre-1978 homes.',
      'Yes. We work to the Massachusetts lead-safe renovation rules on pre-1978 homes, which is '
      'the programme that applies here rather than the federal one.'],
     'Yes. We hold a Lead-Safe Renovation Contractor license from the Massachusetts Department '
     'of Labor Standards, which is the program that applies here rather than the federal one.', 2),
]

manifest = set()
try:
    manifest = set(json.load(open(os.path.join(ROOT, 'mcb-astro', 'published-manifest.json')))['files'])
except Exception:
    pass

# every page a fix names, so we can tell "already patched" from "never matched"
TARGETS = GUARANTEED_PAGES | {f[0] for f in FIXES} | {c[0] for c in CHAIN}

scanned = patched = already = skipped = 0
fails, notes = [], []
seen = set()

for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    if 'index.html' not in fns:
        continue
    p = os.path.join(dp, 'index.html')
    rel = os.path.relpath(p, ROOT).replace('\\', '/')
    if rel in manifest:
        continue
    scanned += 1
    if rel not in TARGETS:
        continue
    seen.add(rel)
    h = open(p, encoding='utf8', newline='').read()
    orig = h

    # ---- 1. the triplicated guarantee ----
    if rel in GUARANTEED_PAGES:
        n = h.count(GUARANTEED)
        if n == 3:
            for new in GUARANTEED_NEW:
                h = h.replace(GUARANTEED, new, 1)
        elif n == 0:
            pass                                  # already patched
        else:
            skipped += 1
            notes.append(f'SKIP {rel}: expected 3 guarantee lines, found {n} — page changed, not touching it')

    # ---- 2-5. exact-string fixes with an asserted count ----
    for frag, old, new, want in FIXES:
        if rel != frag:
            continue
        n = h.count(old)
        if n == want:
            h = h.replace(old, new)
        elif n == 0:
            if new not in h:
                skipped += 1
                notes.append(f'SKIP {rel}: neither "{old[:40]}" nor its replacement found — page changed')
        else:
            skipped += 1
            notes.append(f'SKIP {rel}: expected {want} of "{old[:40]}", found {n} — not touching it')

    # ---- 6. lead-safe credential, whichever wording this file currently carries ----
    for frag, olds, new, want in CHAIN:
        if rel != frag:
            continue
        hit = [o for o in olds if h.count(o) == want]
        if hit:
            h = h.replace(hit[0], new)
        elif new not in h:
            skipped += 1
            found = {o[:34]: h.count(o) for o in olds}
            notes.append(f'SKIP {rel}: no known lead-safe wording at the expected count {want} - {found}')

    if h == orig:
        already += 1
        continue
    try:
        open(p, 'w', encoding='utf8', newline='').write(h)
        patched += 1
    except Exception as e:
        fails.append((rel, str(e)))

for t in sorted(TARGETS - seen):
    notes.append(f'SKIP {t}: file not found under {ROOT}')

print(f'patch_compliance2: {scanned} static page(s) scanned, {patched} patched, '
      f'{already} already patched, {skipped} skipped')
for n in notes:
    print('  ' + n)
for r, e in fails:
    print(f'  FAIL {r}: {e}')
sys.exit(1 if fails else 0)
