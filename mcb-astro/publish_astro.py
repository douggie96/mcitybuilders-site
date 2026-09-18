#!/usr/bin/env python3
"""Publish the Astro build INTO the static site that Vercel actually serves.

Why this exists: Vercel project `site` serves the repo root as plain static files.
It has no build step, and mcb-astro/dist is gitignored. Merging the Astro SOURCE
to main therefore publishes nothing. This script copies the BUILT pages into the
repo root so they ship as ordinary static files next to the existing 126 pages.

Deliberately NOT published: dist/index.html (the Astro homepage). The live
homepage holds #1 for "general contractor lancaster ma"; swapping it is a separate,
reviewed decision. Run with --with-homepage to include it.

Hard stops (exit 1, nothing half-done is committed by DEPLOY.bat):
  * a built file would overwrite an existing site file this script did not create
  * a banned compliance word appears in anything about to be published
"""
import os, re, sys, json, shutil, datetime, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, 'dist')
ROOT = os.path.dirname(HERE)
MANIFEST = os.path.join(HERE, 'published-manifest.json')
WITH_HOME = '--with-homepage' in sys.argv
SKIP_ROOT_FILES = {'robots.txt', 'sitemap.xml', 'sitemap-index.xml', 'sitemap-0.xml', 'favicon.ico', 'favicon.svg'}
BANNED = re.compile(r"\b(licen[cs]ed|insured|bonded|carries insurance)\b|\b(HIC|CSL)\b|\broof\w*", re.I)

def sha(p):
    with open(p, 'rb') as f: return hashlib.sha1(f.read()).hexdigest()

if not os.path.isdir(DIST):
    sys.exit('FAIL: mcb-astro/dist does not exist. Run "npm run build" first.')

prev = set(json.load(open(MANIFEST))['files']) if os.path.exists(MANIFEST) else set()
plan, fails, pages = [], [], []
for dp, _, fns in os.walk(DIST):
    for fn in fns:
        src = os.path.join(dp, fn)
        rel = os.path.relpath(src, DIST).replace('\\', '/')
        if rel == 'index.html' and not WITH_HOME: continue
        if '/' not in rel and rel in SKIP_ROOT_FILES: continue
        dst = os.path.join(ROOT, *rel.split('/'))
        if os.path.exists(dst) and rel not in prev and sha(dst) != sha(src):
            fails.append(f'COLLISION: {rel} already exists in the live site and was not published by this script')
        if rel.endswith('.html'):
            h = open(src, encoding='utf8').read()
            m = BANNED.search(h)
            if m: fails.append(f'BANNED WORD "{m.group(0)}" in {rel}')
            if rel.endswith('/index.html'): pages.append('/' + rel[:-len('/index.html')])
        plan.append((src, dst, rel))

if fails:
    print('\n'.join(fails)); sys.exit(f'\nFAIL: {len(fails)} problem(s). Nothing was copied.')

for src, dst, rel in plan:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
json.dump({'files': sorted(r for _, _, r in plan)}, open(MANIFEST, 'w'), indent=0)
print(f'copied {len(plan)} files ({len(pages)} pages) into the site root')

# ---- sitemap.xml: append any published page that is not already listed ----
sm_path = os.path.join(ROOT, 'sitemap.xml')
sm = open(sm_path, encoding='utf8').read()
have = set(re.findall(r'<loc>https://mcitybuilders\.com([^<]*)</loc>', sm))
today = datetime.date.today().isoformat()
new = [p for p in sorted(pages) if p not in have]
if new:
    block = '  <!-- Astro town + painting pages (publish_astro.py) -->\n' + ''.join(
        f'  <url>\n    <loc>https://mcitybuilders.com{p}</loc>\n    <lastmod>{today}</lastmod>\n'
        f'    <changefreq>monthly</changefreq>\n    <priority>{"0.7" if p.endswith("-ma") else "0.6"}</priority>\n  </url>\n' for p in new)
    sm = sm.replace('</urlset>', block + '</urlset>')
    open(sm_path, 'w', encoding='utf8', newline='\n').write(sm)
print(f'sitemap: +{len(new)} URLs, {len(re.findall("<loc>", sm))} total')

# ---- /areas-we-serve: a crawlable link hub, otherwise the new pages are an island ----
# Nothing in the existing site links to them. Without this they are sitemap-only orphans.
towns = {}
for p in pages:
    m = re.match(r'/(general-contractor|kitchen-remodeling|bathroom-remodeling)-(.+)-ma$', p)
    if m: towns.setdefault(m.group(2), set()).add(m.group(1))
def nice(slug): return ' '.join(w.capitalize() for w in slug.split('-'))
rows = ''.join(
    f'<li style="margin:0 0 10px;color:#C0C0C0"><strong style="color:#fff">{nice(t)}</strong> &mdash; '
    + ' &middot; '.join(f'<a href="/{s}-{t}-ma" style="color:#E63946">{lbl}</a>'
        for s, lbl in (('general-contractor', 'general contractor'), ('kitchen-remodeling', 'kitchens'), ('bathroom-remodeling', 'bathrooms')) if s in svcs)
    + '</li>' for t, svcs in sorted(towns.items()))
paint = ('<p style="color:#C0C0C0;margin:24px 0 0">Painting guides: <a href="/painting" style="color:#E63946">painting in Central Massachusetts</a></p>'
         if '/painting' in pages else '')
hub = ('<!-- ASTRO-HUB:START --><section style="padding:64px 24px;background:#0a0a0a"><div style="max-width:1100px;margin:0 auto">'
       '<h2 style="color:#fff;font-size:1.8rem;font-weight:800;margin:0 0 8px">More towns we work in</h2>'
       '<p style="color:#C0C0C0;margin:0 0 24px">Each page below is written for that town: its housing stock and what a renovation there involves.</p>'
       f'<ul style="list-style:none;padding:0;margin:0;columns:2 300px;column-gap:40px">{rows}</ul>{paint}</div></section><!-- ASTRO-HUB:END -->')
aws = os.path.join(ROOT, 'areas-we-serve', 'index.html')
h = open(aws, encoding='utf8', newline='').read()
h = re.sub(r'<!-- ASTRO-HUB:START -->.*?<!-- ASTRO-HUB:END -->', '', h, flags=re.S)
if '<footer' not in h: sys.exit('FAIL: could not find <footer in areas-we-serve/index.html')
i = h.index('<footer')
open(aws, 'w', encoding='utf8', newline='').write(h[:i] + hub + h[i:])
print(f'areas-we-serve: hub injected, {len(towns)} towns, {sum(len(v) for v in towns.values())} links')

# ---- keep the Astro source tree off the public site ----
vi = os.path.join(ROOT, '.vercelignore')
cur = open(vi, encoding='utf8').read() if os.path.exists(vi) else ''
if 'mcb-astro' not in cur:
    open(vi, 'w', encoding='utf8', newline='\n').write(cur.rstrip('\n') + '\nmcb-astro/\n')
    print('.vercelignore: added mcb-astro/')
print('PUBLISH OK')
