import re, json, glob, os, sys, collections, difflib
DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

files = sorted(glob.glob(os.path.join(DIST,'**','index.html'), recursive=True))
fails, warns = [], []
titles, descs, h1s, bodies = {}, {}, {}, {}

def text_of(h):
    b = re.search(r'<body[^>]*>(.*?)</body>', h, re.S)
    t = b.group(1) if b else h
    t = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()

for f in files:
    url = '/' + os.path.relpath(os.path.dirname(f), DIST)
    url = '/' if url == '/.' else url
    h = open(f, encoding='utf-8').read()

    t = re.search(r'<title>(.*?)</title>', h, re.S)
    t = t.group(1).strip() if t else ''
    d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
    d = d.group(1).strip() if d else ''
    titles[url], descs[url] = t, d

    if not (0 < len(t) <= 60): fails.append(f'{url}: title {len(t)} chars')
    if not (70 <= len(d) <= 160): fails.append(f'{url}: description {len(d)} chars')

    c = re.findall(r'<link rel="canonical" href="([^"]+)"', h)
    if len(c) != 1: fails.append(f'{url}: {len(c)} canonicals')
    elif not c[0].startswith('https://mcitybuilders.com'): fails.append(f'{url}: bad canonical {c[0]}')

    hh = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    if len(hh) != 1: fails.append(f'{url}: {len(hh)} H1s')
    else: h1s[url] = re.sub(r'<[^>]+>', ' ', hh[0]).strip()

    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(b)
        except Exception as e: fails.append(f'{url}: JSON-LD parse {e}')

    if re.search(r'\broof(?:ing|er|ers)?\b', h, re.I): fails.append(f'{url}: ROOFING language present')
    if re.search(r'\b(HIC|CSL)\s*#?\s*\d', h, re.I): fails.append(f'{url}: license number leaked')
    if '1171 Main St' not in h: fails.append(f'{url}: street address missing')
    if 'tel:+15086567436' not in h: fails.append(f'{url}: phone link missing')
    if 'name="twitter:card"' not in h: fails.append(f'{url}: twitter:card missing')

    imgs = re.findall(r'<img[^>]*>', h)
    if [i for i in imgs if 'alt=' not in i]: fails.append(f'{url}: img missing alt')
    if [i for i in imgs if not ('width=' in i and 'height=' in i)]: fails.append(f'{url}: img missing dimensions')

    body = text_of(h)
    bodies[url] = body
    wc = len(body.split())
    if wc < 450: warns.append(f'{url}: only {wc} words')

# ---- uniqueness: the real risk with templated pages
def dupes(d):
    r = collections.defaultdict(list)
    for k, v in d.items(): r[v].append(k)
    return {v: ks for v, ks in r.items() if len(ks) > 1}

for label, d in (('title', titles), ('description', descs), ('H1', h1s)):
    for val, urls in dupes(d).items():
        fails.append(f'DUPLICATE {label} on {len(urls)} pages: {urls[:3]}')

# ---- near-duplicate body text between same-service pages in different towns
svc_groups = collections.defaultdict(list)
for url in bodies:
    m = re.match(r'^/(general-contractor|kitchen-remodeling|bathroom-remodeling)-', url)
    if m: svc_groups[m.group(1)].append(url)

# Sentence-level overlap is what actually matters: character-frequency ratios
# call any two pages of English 97% similar and tell you nothing.
def sents(t):
    return {x.strip() for x in re.split(r'(?<=[.!?]) +', t) if len(x.strip()) > 45}

uniq_report = []
for svc, urls in svc_groups.items():
    allsent = [sents(bodies[u]) for u in urls]
    for i, u in enumerate(urls):
        mine = allsent[i]
        others = set().union(*[allsent[j] for j in range(len(urls)) if j != i]) if len(urls) > 1 else set()
        only = mine - others
        frac = len(only) / max(1, len(mine))
        uniq_report.append((frac, u, len(only), len(mine)))
uniq_report.sort()
if uniq_report:
    print('Sentence uniqueness vs same-service siblings:')
    for frac, u, a, b in uniq_report[:3]:
        print('   lowest: %5.1f%%  (%d of %d sentences unique)  %s' % (frac * 100, a, b, u))
    best = uniq_report[-1]
    print('   highest: %5.1f%%  %s' % (best[0] * 100, best[1]))
    med = uniq_report[len(uniq_report) // 2]
    print('   median:  %5.1f%%' % (med[0] * 100))
    thin = [r for r in uniq_report if r[0] < 0.40]
    if thin:
        fails.append(f'{len(thin)} pages have under 40% unique sentences vs their same-service siblings')

print('=' * 64)
print('BUILT-SITE VERIFICATION —', len(files), 'pages')
print('=' * 64)
for f in fails: print('  FAIL  ' + f)
for w in warns[:10]: print('  WARN  ' + w)
if len(warns) > 10: print('  WARN  ...and %d more' % (len(warns) - 10))
wcs = sorted(len(b.split()) for b in bodies.values())
print(f'\n  word count: min {wcs[0]}  median {wcs[len(wcs)//2]}  max {wcs[-1]}')
print(f'  unique titles {len(set(titles.values()))}/{len(titles)} · '
      f'descriptions {len(set(descs.values()))}/{len(descs)} · H1s {len(set(h1s.values()))}/{len(h1s)}')
print(f'\n  {len(warns)} warnings, {len(fails)} failures')
sys.exit(1 if fails else 0)
