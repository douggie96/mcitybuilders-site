#!/usr/bin/env python3
"""Day 72 claims-compliance pass: image renames, honest alt text, footer disclosure,
portfolio rebuild.  Idempotent -- safe to re-run.

Filenames and alt text may not present illustrative (AI/stock) imagery as a job
Maverick City Builders completed in a named town.  New names describe the subject,
verified by opening each image.
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img')

# old base name -> new base name.  New names were chosen after opening each image;
# several old names did not even match their subject (see the audit notes).
RENAMES = {
    'ai-outdoor-living-space-in-bolton-ma':                       'ai-pergola-deck-outdoor-seating',
    'bathroom-addition-and-title-v-septic-in-central-massachuse': 'white-kitchen-island-pendant-lights',
    'bathroom-remodeling-in-worcester-county-ma':                 'bathroom-freestanding-tub-glass-shower',
    'bathroom-remodeling-project-in-lancaster-ma':                'bathroom-double-vanity-subway-tile-shower',
    'custom-deck-building-project-in-clinton-ma':                 'wrap-around-deck-white-railing',
    'custom-deck-building-project-in-lancaster-ma':               'composite-deck-cable-railing',
    'exterior-repaint-in-worcester-county-ma':                    'composite-deck-riser-lighting',
    'how-to-plan-your-spring-renovation-projects-early':          'modern-dark-kitchen-marble-backsplash',
    'interior-painting-project-in-lancaster-ma':                  'formal-living-room-painted-trim',
    'kitchen-remodeling-project-in-clinton-ma':                   'white-shaker-kitchen-quartz',
    'kitchen-remodeling-project-in-lancaster-ma':                 'white-inset-kitchen-marble-brass',
    'kitchen-remodeling-project-in-leominster-ma':                'cream-kitchen-butcher-block-island',
    'last-chance-for-exterior-projects-before-winter-hits':       'open-plan-interior-glass-wall',
    'living-room-sterling-ma':                                    'great-room-coffered-ceiling-built-ins',
    'master-suite-bolton-ma':                                     'living-room-stone-fireplace-built-ins',
    'trim-and-siding-repaint-in-central-ma':                      'covered-deck-outdoor-kitchen',
}

# (page, old alt/title value) -> new value.  Illustrative alt may not carry a
# service-area town, "Worcester County", "Central MA", "project", or "we built".
ALTS = {
    'about/index.html': {
        'About Maverick City Builders': 'New home framing at dusk',
        'Douglas Mourao, Founder of Maverick City Builders': 'New home framing at dusk',
        'Maverick City Builders Team': 'Residential construction site — design illustration',
    },
    'areas-we-serve/index.html': {
        'Central Massachusetts Construction': 'Residential construction site — design illustration',
    },
    'bathroom-remodeling/index.html': {
        'Bathroom Remodeling in Worcester County, MA': 'Bathroom with a freestanding tub and glass shower enclosure',
    },
    'deck-building/index.html': {
        'Outdoor Living Space in Bolton, MA': 'Pergola over a composite deck with outdoor seating',
        'Composite Deck in Sterling, MA': 'Composite deck with a glass railing at sunset',
        'Custom Deck Building in Massachusetts': 'Custom composite deck with a glass railing',
    },
    'exterior-painting/index.html': {
        'Exterior Repaint in Worcester County MA': 'Composite deck with recessed riser lighting at dusk',
        'Trim and Siding Repaint in Central MA': 'Covered deck with a built-in outdoor kitchen',
        'Exterior Painting Services in Massachusetts': 'Shingled home exterior with a wraparound deck at sunset',
    },
    'general-renovations/index.html': {
        'Whole-Home Renovation in Worcester County': 'Shingled Cape with a landscaped front yard',
        'Whole-home renovation in Worcester County, Massachusetts': 'Shingled Cape with a landscaped front yard',
    },
    'interior-painting/index.html': {
        'Living Room, Sterling MA': 'Great room with a coffered ceiling and built-in cabinetry',
        'Master Suite, Bolton MA': 'Living room with a stone fireplace and built-in shelving',
        'Interior Painting in Massachusetts': 'Formal living room with painted trim and a fireplace',
    },
    'kitchen-remodeling/index.html': {
        'Kitchen Remodeling in Worcester County, MA': 'Modern kitchen with a marble backsplash and integrated appliances',
    },
    'services/index.html': {
        'Our Services': 'Residential construction site — design illustration',
    },
}

DISCLOSURE = ('Some images on this site are design illustrations, including AI-generated concepts, '
              'and are not photographs of Maverick City Builders projects. Photos of our own work '
              'are labelled as such.')
DISCLOSURE_HTML = ('<div class="container mt-6 text-center text-xs text-gray-500">'
                   '<p>' + DISCLOSURE + '</p></div>')

# Straight claim removals that survived the copy pass.
COPY_FIXES = [
    ('general-contractor-worcester-ma/index.html',
     'Maverick City Builders has completed projects across Worcester neighborhoods including',
     'Maverick City Builders serves Worcester neighborhoods including'),
    ('building-restoration/index.html',
     'We&#x27;ve worked with most major Massachusetts insurance carriers.',
     'Restoration work is routinely coordinated with homeowners&#x27; insurance carriers.'),
    ('building-restoration/index.html',
     "We've worked with most major Massachusetts insurance carriers.",
     "Restoration work is routinely coordinated with homeowners' insurance carriers."),
]

PORTFOLIO_SUBHEAD = ('Kitchen, bathroom, deck and whole-home remodeling across Worcester County '
                     'and Central Massachusetts.')
PORTFOLIO_SECTION = (
    '<section class="py-24"><div class="container max-w-3xl">'
    '<h2 class="font-heading text-3xl md:text-4xl font-bold mb-6 tracking-tight">Our Own Job Photos Are Coming Here</h2>'
    '<p class="text-gray-300 font-light leading-relaxed text-lg mb-6">We&#x27;re building this page from our own '
    'job photos. Ask us for references and photos from recent work in your town.</p>'
    '<p class="text-gray-400 font-light leading-relaxed text-sm">' + DISCLOSURE + '</p>'
    '</div></section>')


def read(p):
    return open(p, encoding='utf-8').read()


def write(p, s):
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)


def html_files():
    return sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True))


def text_files():
    out = list(html_files())
    for name in ('sitemap.xml', 'llms.txt', 'robots.txt', 'vercel.json'):
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            out.append(p)
    return out


def step_rename_files():
    moved = []
    for old, new in RENAMES.items():
        for p in sorted(os.listdir(IMG)):
            if p == old + '.jpg' or re.fullmatch(re.escape(old) + r'-(480|800|1408|768|1200)\.webp', p):
                dst = p.replace(old, new, 1)
                src_p, dst_p = os.path.join(IMG, p), os.path.join(IMG, dst)
                if os.path.exists(dst_p):
                    continue
                os.rename(src_p, dst_p)
                moved.append((p, dst))
    return moved


def step_rewrite_refs():
    n = 0
    for f in text_files():
        s = orig = read(f)
        for old, new in RENAMES.items():
            s = s.replace(old, new)
        if s != orig:
            write(f, s)
            n += 1
    return n


def step_redirects():
    p = os.path.join(ROOT, 'vercel.json')
    cfg = json.loads(read(p))
    have = {r.get('source') for r in cfg['redirects']}
    added = 0
    for old, new in RENAMES.items():
        src = '/assets/img/%s.jpg' % old
        if src in have:
            continue
        cfg['redirects'].append({'source': src,
                                 'destination': '/assets/img/%s.jpg' % new,
                                 'permanent': True})
        added += 1
    if added:
        write(p, json.dumps(cfg, indent=2) + '\n')
    return added


def step_alts():
    n = 0
    for rel, mapping in ALTS.items():
        p = os.path.join(ROOT, rel)
        s = orig = read(p)
        for old, new in mapping.items():
            s = s.replace('alt="%s"' % old, 'alt="%s"' % new)
            s = s.replace('title="%s"' % old, 'title="%s"' % new)
        if s != orig:
            write(p, s)
            n += 1
    return n


def step_disclosure():
    n = 0
    for f in html_files():
        s = read(f)
        if DISCLOSURE in s:
            continue
        if '</footer>' not in s:
            print('  !! no footer:', f)
            continue
        write(f, s.replace('</footer>', DISCLOSURE_HTML + '</footer>', 1))
        n += 1
    return n


def step_copy_fixes():
    n = 0
    for rel, old, new in COPY_FIXES:
        p = os.path.join(ROOT, rel)
        s = read(p)
        if old in s:
            write(p, s.replace(old, new))
            n += 1
    return n


def step_portfolio():
    p = os.path.join(ROOT, 'portfolio', 'index.html')
    s = read(p)
    s = s.replace('Explore our recent projects. Real homes, real transformations.', PORTFOLIO_SUBHEAD)
    start = s.find('<section class="py-24 min-h-[600px]">')
    if start != -1:
        end = s.find('<section class="py-32 bg-[#111] text-center border-t border-white/5">', start)
        if end == -1:
            print('  !! portfolio CTA anchor not found; grid left in place')
            return False
        s = s[:start] + PORTFOLIO_SECTION + s[end:]
    write(p, s)
    return True


if __name__ == '__main__':
    print('renamed files    :', len(step_rename_files()))
    print('files w/ new refs:', step_rewrite_refs())
    print('redirects added  :', step_redirects())
    print('pages alt-fixed  :', step_alts())
    print('copy fixes       :', step_copy_fixes())
    print('portfolio rebuilt:', step_portfolio())
    print('disclosure added :', step_disclosure())
