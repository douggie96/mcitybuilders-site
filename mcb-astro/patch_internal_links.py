#!/usr/bin/env python3
"""Internal-link weight redistribution. Measured 2026-09-20, built the same day.

WHY THIS EXISTS
---------------
GSC Links (2026-09-20): 17 external links, 5 referring domains, all pointing at the
homepage. Internal links are therefore the ONLY mechanism distributing authority on
this site, and the distribution was measured across all 274 deployed pages.

Three of the four defects I first claimed turned out to be wrong, and they are recorded
here so nobody re-derives them:

  WRONG - "the money pages are buried."  They are not. Click depth from the homepage is
          0:1, 1:25, 2:240, 3:7 pages. One orphan. Depth is fine.
  WRONG - "the service pages do not link down to their town variants."  /kitchen-remodeling
          already links to 17 town variants, /bathroom-remodeling to 16, /deck-building to
          6 of 6. The town hubs already link down to their service pages.
  DROPPED - footer legal consolidation.  Four legal links out of ~45 unique links per page
          is about 9% of outgoing equity; removing two returns ~4.5% to everything else.
          That is marginal, it is a user-facing change, and dropping an accessibility link
          from the footer to chase it is a bad trade. Not done.

WHAT IS ACTUALLY WRONG, and what this script fixes:

  /how-to-hire-contractor-massachusetts has 2 inbound internal links and produced 2 clicks
  from 149 impressions - the best impressions-per-inbound-link ratio on the site.
  The /painting/* cluster has 3 inbound links each.
  /composite-deck-installers-central-ma has 1.  /deck-building-cost-massachusetts has 2.
  The 30 blog posts share 53 inbound links between them - a mean of 1.8, min 0, max 3.

Each of those is a high-intent page fed by almost nothing, while the nine service pages
that would link to them carry ~200 inbound links each.

WHAT THIS SCRIPT DELIBERATELY DOES NOT DO
-----------------------------------------
It does not link the 48 kitchen and 48 bathroom outer-ring town pages that their parent
service page skips. Those are part of the cohort of 137 indexed pages that received zero
impressions in 90 days. Spreading a very small authority pool across more pages that have
never ranked is the opposite of the point. Concentrate, do not spread.

MECHANICS
---------
Idempotent - the block carries the marker <!--mcb-rel--> and a second run prints
"already patched". Additive only: nothing existing is removed or rewritten. Every target
URL is verified to exist on disk before a link to it is written; a missing target is
reported as SKIP and the link is dropped rather than shipping a 404.

Reads and writes with newline='' so existing line endings survive untouched.
Wired into DEPLOY.bat step [2b] after patch_compliance2.py.
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

MARK = '<!--mcb-rel-->'
LINK = '<a href="{0}" style="color:#E10600;text-decoration:underline">{1}</a>'

HIRE = ('/how-to-hire-contractor-massachusetts', 'How to hire a contractor in Massachusetts')
PERMITS = ('/building-permits-central-massachusetts',
           'Building permits in Central Massachusetts')

# page -> [(href, anchor text), ...]
PLAN = {
    'kitchen-remodeling': [
        PERMITS,
        ('/kitchen-remodel-cost-worcester-ma', 'Kitchen remodel cost in Worcester'),
        ('/kitchen-remodel-cost-marlborough-ma', 'Kitchen remodel cost in Marlborough'),
        ('/blog/kitchen-remodeling-cost-central-massachusetts', 'What a kitchen remodel costs in Central Massachusetts'),
        ('/blog/kitchen-remodel-permits-timeline-central-ma', 'Kitchen permits and timeline'),
        ('/blog/older-home-kitchen-remodel-surprises-central-ma', 'What older homes hide in a kitchen'),
        ('/blog/opening-up-closed-kitchen-older-home-ma', 'Opening up a closed kitchen'),
        HIRE,
    ],
    'bathroom-remodeling': [
        PERMITS,
        ('/bathroom-remodel-cost-massachusetts', 'Bathroom remodel cost in Massachusetts'),
        ('/blog/small-hall-bathroom-remodel-cost-central-ma', 'Small hall bathroom costs'),
        ('/blog/bathroom-addition-title-v-septic-central-ma', 'Adding a bathroom on a septic system'),
        ('/blog/tile-vs-prefab-shower-surround-ma', 'Tile against a prefab shower surround'),
        ('/blog/walk-in-shower-aging-in-place-bathroom-ma', 'Walk-in showers and aging in place'),
        ('/blog/bathroom-ventilation-moisture-older-homes-ma', 'Ventilation and moisture in older homes'),
        HIRE,
    ],
    'deck-building': [
        PERMITS,
        ('/deck-building-cost-massachusetts', 'Deck building cost in Massachusetts'),
        ('/composite-deck-installers-central-ma', 'Composite deck installation in Central Massachusetts'),
        ('/deck-builders-worcester-county-ma', 'Deck builders in Worcester County'),
        ('/deck-builders-west-sterling-ma', 'Deck builders in West Sterling'),
        HIRE,
    ],
    'interior-painting': [
        ('/interior-painting-cost-massachusetts', 'Interior painting cost in Massachusetts'),
        ('/painting/cabinet-painting', 'Cabinet painting'),
        ('/painting/painting-older-homes-massachusetts', 'Painting older Massachusetts homes'),
        ('/house-painters-worcester-ma', 'House painters in Worcester'),
        ('/house-painters-clinton-ma', 'House painters in Clinton'),
        HIRE,
    ],
    'exterior-painting': [
        ('/exterior-painting-cost-massachusetts', 'Exterior painting cost in Massachusetts'),
        ('/painting/when-to-paint-exterior-massachusetts', 'When to paint an exterior in Massachusetts'),
        ('/blog/right-temperature-exterior-painting-massachusetts', 'The right temperature for exterior paint'),
        ('/blog/is-it-too-cold-to-paint-house-exterior-massachusetts', 'Is it too cold to paint?'),
        ('/blog/signs-your-home-ready-exterior-painting', 'Signs a house is ready for paint'),
        HIRE,
    ],
    'carpentry': [
        PERMITS,
        ('/flooring-installation-lancaster-ma', 'Flooring installation in Lancaster'),
        ('/blog/kitchen-cabinets-1900s-farmhouse-central-ma', 'Cabinets in a 1900s farmhouse'),
        HIRE,
    ],
    'general-renovations': [
        PERMITS,
        ('/structural-repair-worcester-county-ma', 'Structural repair in Worcester County'),
        ('/rot-repair-cost-massachusetts', 'Rot repair cost in Massachusetts'),
        ('/blog/kitchen-remodel-home-value-massachusetts', 'What a remodel adds to home value'),
        HIRE,
    ],
    'building-restoration': [
        ('/structural-repair-worcester-county-ma', 'Structural repair in Worcester County'),
        ('/blog/prevent-ice-dams-massachusetts', 'Preventing ice dams'),
        HIRE,
    ],
    'water-damage-restoration': [
        ('/blog/properly-winterize-home-massachusetts', 'Winterising a Massachusetts home'),
        ('/blog/winter-home-care-tips-avoid-expensive-repairs', 'Winter home care'),
        HIRE,
    ],
}

# Every town hub gets the hire guide plus the two seasonal planning pieces.
HUB_LINKS = [
    HIRE,
    PERMITS,
    ('/blog/how-to-choose-general-contractor-massachusetts', 'Choosing a general contractor'),
    ('/blog/spring-home-maintenance-checklist-massachusetts', 'Spring home maintenance checklist'),
]

HEADING = 'Related guides'


def exists(href):
    rel = href.strip('/').replace('/', os.sep)
    return os.path.isfile(os.path.join(ROOT, rel, 'index.html'))


def block(links):
    items = ''.join('<li style="margin:0 0 6px;">' + LINK.format(h, t) + '</li>' for h, t in links)
    return (MARK + '<section style="max-width:1100px;margin:0 auto;padding:32px 24px;'
            'border-top:1px solid #222;"><h2 style="color:#fff;font-size:1.05rem;'
            'font-weight:700;margin:0 0 12px;">' + HEADING + '</h2>'
            '<ul style="list-style:none;padding:0;margin:0;">' + items + '</ul></section>')


targets = {}
for slug, links in PLAN.items():
    targets[slug] = links
hubs = []
hubdir = os.path.join(ROOT, 'areas-we-serve')
if os.path.isdir(hubdir):
    for name in sorted(os.listdir(hubdir)):
        if os.path.isfile(os.path.join(hubdir, name, 'index.html')):
            hubs.append('areas-we-serve/' + name)
for h in hubs:
    targets[h] = HUB_LINKS

# DEPLOY.bat runs this at step [2b], which is BEFORE publish_astro.py copies the freshly
# built Astro pages into the site root at step [6/8]. Anything patched here that is also
# Astro-published would be silently overwritten by that copy. All 25 targets were verified
# static against published-manifest.json on 2026-09-20; this guard shouts if that changes
# rather than shipping a patch that quietly disappears on the next deploy.
manifest = set()
try:
    manifest = set(json.load(open(os.path.join(
        ROOT, 'mcb-astro', 'published-manifest.json')))['files'])
except Exception:
    pass

patched = already = skipped = 0
notes = []
fails = []
added = 0

for slug, links in sorted(targets.items()):
    rel = slug + '/index.html'
    if rel in manifest:
        notes.append('SKIP %s: Astro-published - publish_astro.py at step [6/8] would '
                     'overwrite this. Move the block into the Astro template instead.' % slug)
        skipped += 1
        continue
    p = os.path.join(ROOT, slug.replace('/', os.sep), 'index.html')
    if not os.path.isfile(p):
        notes.append('SKIP %s: file not found under ROOT' % slug)
        skipped += 1
        continue
    h = open(p, encoding='utf8', newline='').read()

    # A page patched by an earlier run carries MARK. Rather than skipping it -- which would
    # mean a link added to PLAN later never reaches the pages that need it -- top up the
    # existing block with whatever is missing. Idempotent either way: when nothing is
    # missing the file is unchanged and the page counts as already patched.
    topup = MARK in h
    live = []
    for href, text in links:
        if href.strip('/') == slug:
            continue
        if not exists(href):
            notes.append('SKIP link %s on %s: target not on disk' % (href, slug))
            continue
        if ('href="%s"' % href) in h:
            continue          # already linked contextually; do not duplicate
        live.append((href, text))
    if not live:
        already += 1
        continue
    # Prefer inside <main>: links in the main content read as contextual, links between
    # </main> and <footer> read as boilerplate. Fall back to the footer anchor on the
    # pages that have no <main> element (e.g. /water-damage-restoration).
    if topup:
        # insert the missing <li> items at the end of the existing list
        bi = h.find(MARK)
        ei = h.find('</ul>', bi)
        if ei == -1:
            notes.append('SKIP %s: marker present but no </ul> found' % slug)
            skipped += 1
            continue
        items = ''.join('<li style="margin:0 0 6px;">' + LINK.format(href, text) + '</li>'
                        for href, text in live)
        h = h[:ei] + items + h[ei:]
        try:
            open(p, 'w', encoding='utf8', newline='').write(h)
            patched += 1
            added += len(live)
        except Exception as e:
            fails.append((slug, str(e)))
        continue

    i = h.rfind('</main>')
    if i == -1:
        i = h.rfind('<footer')
    if i == -1:
        notes.append('SKIP %s: no </main> or <footer> anchor found' % slug)
        skipped += 1
        continue
    h = h[:i] + block(live) + h[i:]
    try:
        open(p, 'w', encoding='utf8', newline='').write(h)
        patched += 1
        added += len(live)
    except Exception as e:
        fails.append((slug, str(e)))

print('patch_internal_links: %d page(s) patched, %d already patched, %d skipped, '
      '%d internal links added' % (patched, already, skipped, added))
for n in notes:
    print('  ' + n)
for r, e in fails:
    print('  FAIL %s: %s' % (r, e))
sys.exit(1 if fails else 0)
