"""Verify the built output, not the source. Every check is a pass/fail against
the thing Vercel would actually serve."""
import re, json, sys, os

P = '/home/claude/mcb-astro/dist/index.html'
h = open(P, encoding='utf-8').read()
fails, warns, oks = [], [], []

def chk(name, cond, detail=''):
    (oks if cond else fails).append(f'{name}{" — " + detail if detail else ""}')

def warn(name, cond, detail=''):
    if not cond:
        warns.append(f'{name}{" — " + detail if detail else ""}')
    else:
        oks.append(name)

# ---- title / description
t = re.search(r'<title>(.*?)</title>', h, re.S)
title = t.group(1).strip() if t else ''
d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
desc = d.group(1).strip() if d else ''
chk('title present', bool(title))
chk(f'title <=60 chars ({len(title)})', 0 < len(title) <= 60, title)
chk('description present', bool(desc))
chk(f'description 70-160 chars ({len(desc)})', 70 <= len(desc) <= 160)

# ---- canonical
c = re.findall(r'<link rel="canonical" href="([^"]+)"', h)
chk('exactly one canonical', len(c) == 1, str(c))
chk('canonical is absolute https', bool(c) and c[0].startswith('https://mcitybuilders.com'), c[0] if c else '')
chk('canonical has no trailing slash', bool(c) and not c[0].endswith('/') or c == ['https://mcitybuilders.com'], c[0] if c else '')

# ---- headings
h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S)
chk(f'exactly one H1 ({len(h1)})', len(h1) == 1)
chk('H1 != title', bool(h1) and re.sub(r'<[^>]+>', ' ', h1[0]).strip() != title)
h2 = re.findall(r'<h2[^>]*>', h)
chk(f'has H2s ({len(h2)})', len(h2) >= 3)

# ---- JSON-LD
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
parsed, types = [], []
for b in blocks:
    try:
        o = json.loads(b); parsed.append(o); types.append(o.get('@type'))
    except Exception as e:
        fails.append(f'JSON-LD parse error: {e}')
chk(f'JSON-LD blocks parse ({len(parsed)}/{len(blocks)})', len(parsed) == len(blocks) and len(blocks) > 0)
chk('GeneralContractor schema present', 'GeneralContractor' in types, str(types))
chk('FAQPage schema present', 'FAQPage' in types, str(types))

gc = next((o for o in parsed if o.get('@type') == 'GeneralContractor'), None)
if gc:
    a = gc.get('address', {})
    chk('schema has streetAddress', a.get('streetAddress') == '1171 Main St', str(a.get('streetAddress')))
    chk('schema locality Lancaster', a.get('addressLocality') == 'Lancaster')
    chk('schema region MA', a.get('addressRegion') == 'MA')
    chk('schema postal 01523', a.get('postalCode') == '01523')
    chk('schema telephone present', bool(gc.get('telephone')))
    chk('schema geo present', 'geo' in gc)
else:
    fails.append('no GeneralContractor block to inspect')

faq = next((o for o in parsed if o.get('@type') == 'FAQPage'), None)
if faq:
    qs = [q['name'] for q in faq.get('mainEntity', [])]
    body = re.sub(r'<[^>]+>', ' ', h)
    missing = [q for q in qs if q not in body]
    chk(f'every FAQ question is in visible text ({len(qs)} Qs)', not missing, str(missing))
    sem = re.findall(r'<summary[^>]*>\s*<h3[^>]*>(.*?)</h3>', h, re.S)
    chk(f'FAQs use semantic summary/h3 markup ({len(sem)})', len(sem) >= len(qs))

# ---- social
chk('og:title', 'property="og:title"' in h)
chk('og:description', 'property="og:description"' in h)
chk('og:url', 'property="og:url"' in h)
chk('twitter:card', 'name="twitter:card"' in h)

# ---- NAP on page
chk('phone link present', 'tel:+15086567436' in h)
chk('street address in visible copy', '1171 Main St' in h)
chk('no HIC/CSL numbers leaked', not re.search(r'\b(HIC|CSL)\s*#?\s*\d', h, re.I))

# ---- Phase-3 towns must not appear (Rule 3)
banned = ['Wellesley', 'Dover', 'Wayland', 'Natick', 'Sherborn', 'Weston']
present = [b for b in banned if re.search(r'\b' + b + r'\b', h)]
chk('no Phase-3 towns', not present, str(present))

# ---- roofing must never appear
roof = re.findall(r'\broof(?:ing|er|ers)?\b', h, re.I)
chk('no roofing service language', not roof, str(set(roof)))

# ---- images
imgs = re.findall(r'<img[^>]*>', h)
no_alt = [i for i in imgs if 'alt=' not in i]
no_dim = [i for i in imgs if not ('width=' in i and 'height=' in i)]
chk(f'all images have alt ({len(imgs)} imgs)', not no_alt, f'{len(no_alt)} missing')
chk('all images have width+height', not no_dim, f'{len(no_dim)} missing')
lazy = [i for i in imgs if 'loading="lazy"' in i]
warn(f'most images lazy-loaded ({len(lazy)}/{len(imgs)})', len(lazy) >= len(imgs) - 3)

# ---- crawlability: content must exist without JS
body = re.search(r'<body[^>]*>(.*?)</body>', h, re.S).group(1)
text = re.sub(r'<script.*?</script>', ' ', body, flags=re.S)
text = re.sub(r'<style.*?</style>', ' ', text, flags=re.S)
words = len(re.sub(r'<[^>]+>', ' ', text).split())
chk(f'server-rendered word count ({words})', words >= 400)
chk('hero copy is real DOM, not canvas-only', 'Studs to' in text)

# ---- accessibility basics that also affect SEO
chk('skip link', 'class="skip"' in h)
chk('lang attribute', 'lang="en"' in h)
chk('main landmark', '<main' in h)

# ---- perf
js = re.findall(r'<script(?![^>]*ld\+json)[^>]*>(.*?)</script>', h, re.S)
jsbytes = sum(len(x) for x in js)
warn(f'inline JS under 12KB ({jsbytes}B)', jsbytes < 12000)
chk('no render-blocking external JS', not re.search(r'<script[^>]+src="https?://(?!www\.googletagmanager)', h))

print('=' * 62)
print('BUILT-OUTPUT SEO VERIFICATION —', os.path.basename(P))
print('=' * 62)
for f in fails: print('  FAIL  ' + f)
for w in warns: print('  WARN  ' + w)
print(f'\n  {len(oks)} passed, {len(warns)} warnings, {len(fails)} failures')
sys.exit(1 if fails else 0)
