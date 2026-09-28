#!/usr/bin/env python3
"""Inject an 'ideas' gallery (swatch + room card per sub-service page) into the legacy
static hub pages /deck-building and /carpentry, which are not Astro pages.
Idempotent: replaces any previous block between the MCB-IDEAS markers.
Usage: python3 inject_ideas_galleries.py <site_root>   (site_root = folder holding deck-building/index.html)
Images are AI design-idea illustrations; the block says so."""
import sys, os, re, glob, html
import yaml
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
HUBS = {'deck-building': ('decks', 'Deck ideas'), 'carpentry': ('carpentry', 'Carpentry ideas')}
def fm(p):
    t = open(p, encoding='utf-8').read(); return yaml.safe_load(t.split('---', 2)[1])
for hub, (trade, heading) in HUBS.items():
    page = os.path.join(ROOT, hub, 'index.html')
    docs = sorted((fm(p) | {'slug': os.path.basename(p)[:-3]} for p in glob.glob(os.path.join(HERE, 'src/content/ideas', trade, '[!_]*.md'))), key=lambda d: d['order'])
    intro = open(os.path.join(HERE, 'src/content/ideas', trade, '_hub_intro.md'), encoding='utf-8').read().strip()
    e = html.escape
    short = lambda h: re.sub(r' in (Central )?(MA|Massachusetts)$', '', h, flags=re.I)
    cards = ''.join(f'''<li><a class="mi-card" href="/{hub}/{d['slug']}"><span class="mi-pair"><img src="{e(d['swatch'])}" alt="{e(d['swatchAlt'])}" width="800" height="800" loading="lazy" decoding="async"><img src="{e(d['image'])}" alt="{e(d['imageAlt'])}" width="1600" height="1195" loading="lazy" decoding="async"></span><span class="mi-txt"><strong>{e(short(d['h1']))}</strong><span>{e(d['card'])}</span><span class="mi-cost">{('Typical: ' if '$' in d['costRange'] else '') + e(d['costRange'])}</span></span></a></li>''' for d in docs)
    block = f'''<!--MCB-IDEAS-START--><style>.mi-wrap{{max-width:1200px;margin:0 auto;padding:56px 24px;color:#fff}}.mi-wrap h2{{font-size:1.9rem;font-weight:800;margin:0 0 10px}}.mi-wrap p{{color:#bbb;max-width:70ch;line-height:1.6}}.mi-grid{{list-style:none;padding:0;margin:24px 0 0;display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr))}}.mi-card{{display:block;height:100%;background:#111;border:1px solid #2a2a2a;color:#fff;text-decoration:none;transition:border-color .2s}}.mi-card:hover,.mi-card:focus-visible{{border-color:#E10600}}.mi-pair{{display:grid;grid-template-columns:1fr 1.6fr;gap:2px;background:#2a2a2a}}.mi-pair img{{width:100%;height:180px;object-fit:cover;display:block}}.mi-txt{{display:grid;gap:6px;padding:14px 16px 16px}}.mi-txt strong{{font-size:1.15rem}}.mi-txt span{{color:#ccc;font-size:.95rem}}.mi-txt .mi-cost{{font-family:ui-monospace,monospace;font-size:.8rem;color:#999}}.mi-note{{font-size:.8rem!important;color:#888!important;margin-top:14px}}</style>
<section class="mi-wrap" aria-labelledby="mi-h-{trade}"><h2 id="mi-h-{trade}">{e(heading)}</h2><p>{e(intro)}</p><ul class="mi-grid">{cards}</ul><p class="mi-note">Photos are AI design-idea illustrations, not photos of Maverick City Builders projects.</p></section><!--MCB-IDEAS-END-->'''
    h = open(page, encoding='utf-8').read()
    h = re.sub(r'<!--MCB-IDEAS-START-->.*?<!--MCB-IDEAS-END-->', '', h, flags=re.S)
    anchor = h.find('<section style=')           # first of the appended "related guides" blocks
    if anchor < 0: anchor = h.find('</main>')
    if anchor < 0: sys.exit(f'FAIL: no anchor in {page}')
    h = h[:anchor] + block + h[anchor:]
    open(page, 'w', encoding='utf-8').write(h)
    print(f'{hub}: injected {len(docs)} cards')
