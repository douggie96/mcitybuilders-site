import re, json, glob, os, sys, collections, html
ROOT = os.path.dirname(os.path.abspath(__file__))

files = sorted(glob.glob(os.path.join(ROOT,'dist','**','index.html'), recursive=True))
fails, warns = [], []
titles, descs, h1s, bodies, canon_to, raws = {}, {}, {}, {}, {}, {}

def text_of(h):
    b = re.search(r'<body[^>]*>(.*?)</body>', h, re.S)
    t = b.group(1) if b else h
    t = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()

for f in files:
    url = '/' + os.path.relpath(os.path.dirname(f), os.path.join(ROOT,'dist')).replace('\\','/')
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
    else:
        # A canonical may point at itself, or — for a kitchen/bathroom town page only —
        # at the same town's general-contractor page. Anything else is a mistake.
        target = c[0].replace('https://mcitybuilders.com', '').rstrip('/') or '/'
        self_url = url.rstrip('/') or '/'
        m_kb = re.match(r'^/(kitchen-remodeling|bathroom-remodeling)-(.+-ma)$', url)
        if target != self_url:
            if m_kb and target == f'/general-contractor-{m_kb.group(2)}':
                canon_to[url] = target
            else:
                fails.append(f'{url}: canonical points at {target}, which is neither itself nor its town GC page')

    hh = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    if len(hh) != 1: fails.append(f'{url}: {len(hh)} H1s')
    else: h1s[url] = re.sub(r'<[^>]+>', ' ', hh[0]).strip()

    # JSON-LD must parse AND its FAQ content must exist in visible text.
    # Schema that describes content the page does not actually show is a
    # structured-data violation, and the homepage verifier caught this class of
    # problem while this one did not. Closing that gap.
    # html.unescape: Astro writes &#39; / &quot; in visible text while JSON.stringify
    # keeps the raw character in the JSON-LD. Without unescaping, any FAQ answer with
    # an apostrophe in its first 60 characters was a false FAIL (found 2026-09-18).
    vis = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ',
          re.sub(r'<script.*?</script>', ' ', h, flags=re.S))))
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            o = json.loads(b)
        except Exception as e:
            fails.append(f'{url}: JSON-LD parse {e}')
            continue
        if o.get('@type') == 'FAQPage':
            for q in o.get('mainEntity', []):
                qn = re.sub(r'\s+', ' ', q['name']).strip()
                an = re.sub(r'\s+', ' ', q['acceptedAnswer']['text']).strip()
                if qn not in vis:
                    fails.append(f'{url}: FAQ question in schema but not visible: {qn[:60]}')
                elif an[:60] not in vis:
                    fails.append(f'{url}: FAQ answer in schema but not visible: {qn[:60]}')

    if re.search(r'\broof\w*\b', h, re.I): fails.append(f'{url}: ROOFING language present')
    if re.search(r'\b(HIC|CSL)\s*#?\s*\d', h, re.I): fails.append(f'{url}: license number leaked')
    # Douglas withholds the HIC/CSL registration number. Massachusetts HIC
    # advertising rules require that number wherever registration is claimed,
    # so with it withheld NO licensing or insurance claim may appear at all.
    # Checking only for a leaked NUMBER missed 145 pages asserting "Licensed
    # general contractor" and "fully licensed ... and carries insurance".
    claim = re.search(r'\b(licen[cs]ed|fully licen[cs]ed|bonded|carries insurance|insured)\b', h, re.I)
    if claim: fails.append(f'{url}: licensing/insurance CLAIM present ("{claim.group(0)}")')
    if '1171 Main St' not in h: fails.append(f'{url}: street address missing')
    if 'tel:+15086567436' not in h: fails.append(f'{url}: phone link missing')
    if 'name="twitter:card"' not in h: fails.append(f'{url}: twitter:card missing')

    imgs = re.findall(r'<img[^>]*>', h)
    if [i for i in imgs if 'alt=' not in i]: fails.append(f'{url}: img missing alt')
    if [i for i in imgs if not ('width=' in i and 'height=' in i)]: fails.append(f'{url}: img missing dimensions')

    body = text_of(h)
    bodies[url] = body
    raws[url] = h
    wc = len(body.split())
    if wc < 450: warns.append(f'{url}: only {wc} words')

# ---- internal link graph. Programmatic pages that nothing links to do not get
# crawled, which is the most likely way 144 town pages quietly fail.
linkmap, inbound = {}, collections.Counter()
pageset = set(bodies)
for f in files:
    url = '/' + os.path.relpath(os.path.dirname(f), os.path.join(ROOT, 'dist')).replace('\\','/')
    url = '/' if url == '/.' else url
    h = open(f, encoding='utf-8').read()
    outs = {(x.rstrip('/') or '/') for x in re.findall(r'<a[^>]+href="(/[^"#?]*)"', h)}
    linkmap[url] = outs
    for o in outs:
        if o in pageset and o != url:
            inbound[o] += 1
orphans = sorted(p for p in pageset if inbound[p] == 0)
if orphans:
    fails.append(f'{len(orphans)} orphan page(s) with no internal inbound links: {orphans[:5]}')
thin_in = sorted(p for p in pageset if 0 < inbound[p] < 2)
for p in thin_in:
    warns.append(f'{p}: only {inbound[p]} internal inbound link')

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

# ---- SAME-TOWN overlap: kitchen/bathroom page vs that town's general-contractor page.
# The check above compares a page against the SAME SERVICE in OTHER towns and was green
# while the three pages inside one town shared 85-88% of their sentences (09-17 audit).
# It was looking at the wrong pair. This one looks at the right pair.
# Measured the way the audit measured it: header/footer/nav stripped, exact sentence
# match, sentences of 8+ words. A self-canonical K/B page over 40% shared FAILS the
# build. A K/B page that canonicalises to its GC page is allowed over the bar (that
# is the whole point of the canonical) and is reported so the number is visible.
SAME_TOWN_MAX = 0.40
def article_sents(h):
    b = re.search(r'<body[^>]*>(.*?)</body>', h, re.S)
    t = b.group(1) if b else h
    for tag in ('script', 'style', 'header', 'footer', 'nav'):
        t = re.sub(r'<%s\b.*?</%s>' % (tag, tag), ' ', t, flags=re.S | re.I)
    t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()
    return {s.strip() for s in re.split(r'(?<=[.!?]) +', t) if len(s.split()) >= 8}

same_town = []
for url in bodies:
    m = re.match(r'^/(kitchen-remodeling|bathroom-remodeling)-(.+-ma)$', url)
    if not m: continue
    gc = f'/general-contractor-{m.group(2)}'
    if gc not in bodies:
        fails.append(f'{url}: no general-contractor page for this town ({gc})'); continue
    mine, theirs = article_sents(raws[url]), article_sents(raws[gc])
    shared = len(mine & theirs) / max(1, len(mine))
    same_town.append((shared, url, len(mine & theirs), len(mine), url in canon_to))
same_town.sort(reverse=True)
if same_town:
    over_self = [r for r in same_town if r[0] > SAME_TOWN_MAX and not r[4]]
    over_canon = [r for r in same_town if r[0] > SAME_TOWN_MAX and r[4]]
    under = [r for r in same_town if r[0] <= SAME_TOWN_MAX]
    med = same_town[len(same_town) // 2]
    print('Same-town overlap (kitchen/bathroom page vs its town GC page, 8+ word sentences):')
    print('   highest: %5.1f%%  (%d of %d sentences shared)  %s' % (same_town[0][0] * 100, same_town[0][2], same_town[0][3], same_town[0][1]))
    print('   median:  %5.1f%%   lowest: %5.1f%%  %s' % (med[0] * 100, same_town[-1][0] * 100, same_town[-1][1]))
    print('   %d pages canonicalise to their GC page (%d of them over %d%% shared)' % (len(canon_to), len(over_canon), SAME_TOWN_MAX * 100))
    print('   %d pages are under %d%% shared and could stand on their own' % (len(under), SAME_TOWN_MAX * 100))
    ready = [r for r in under if r[4]]
    for r in ready[:10]:
        print('     READY to self-canonical (%4.1f%%): %s' % (r[0] * 100, r[1]))
    if over_self:
        fails.append(f'{len(over_self)} self-canonical kitchen/bathroom pages share over {int(SAME_TOWN_MAX*100)}% of sentences with their town GC page: {[r[1] for r in over_self[:5]]}')

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
