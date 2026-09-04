#!/usr/bin/env python3
"""Generate tools/image_provenance.json.

Buckets every content asset in assets/img/ as `real` (MCB's own photograph of an
MCB job, homeowner-approved) or `illustrative` (AI-generated or stock imagery, and
design concepts).  Only `real` assets may carry a town name, the word "project",
"we built"/"we completed", or appear in an "our work" context.

Visual inspection 2026-09-03 (Day 72) established that NO asset currently in
assets/img/ is a photograph of an MCB job.  The two assets previously presumed
real -- maverick-city-builders-team and about-maverick-city-builders -- were
opened and are AI/stock: a glass hillside mansion with a tower crane over a
big-city skyline, and a timber-framed house shell at night.  Neither is
Massachusetts, neither is MCB's crew, and neither is a portrait of the founder.
Real MCB job photography lives outside this directory in JOBS/_WEB_READY/ and is
published only after Doug approves each set.
"""
import json, os, re, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, 'assets', 'img')
VARIANT = re.compile(r'-(480|800|1408|768|1200)\.(webp|jpg)$|\.(jpg|jpeg|webp|png|svg|ico)$')

# Assets that are not page content: chrome, icons, share cards.
NON_CONTENT = {
    'logo', 'favicon-32', 'apple-touch-icon', 'favicon',
    'maverick-city-builders', 'social-share-card', 'hero',
}

# Every content asset is illustrative until Doug approves a real job set.
# reason is recorded per asset so a future session does not have to re-derive it.
REASONS = {
    'ai-luxury-shaker-kitchen': 'AI-generated concept (ai- prefix).',
    'ai-open-concept-living-area': 'AI-generated concept (ai- prefix).',
    'ai-spa-like-master-bath': 'AI-generated concept (ai- prefix).',
    'ai-outdoor-living-space': 'AI-generated concept (ai- prefix). Renamed off Bolton.',
    'maverick-city-builders-team': 'AI/stock: glass hillside mansion, tower crane, big-city skyline. Not MCB, not MA.',
    'about-maverick-city-builders': 'AI/stock: timber-framed house shell at night. Not a portrait of the founder.',
}
DEFAULT_REASON = 'Stock or AI imagery. No MCB job photography on disk matches it.'


def main():
    names = collections.OrderedDict()
    for p in sorted(os.listdir(IMGDIR)):
        base = VARIANT.sub('', p)
        if base in NON_CONTENT:
            continue
        names.setdefault(base, [])
        names[base].append(p)

    # where each asset is placed
    used = collections.defaultdict(set)
    for f in sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)):
        html = open(f, encoding='utf-8').read()
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        for m in re.finditer(r'/assets/img/([^"\'\s)]+)', html):
            used[VARIANT.sub('', os.path.basename(m.group(1)))].add(rel)

    out = {
        '_generated': '2026-09-03',
        '_standard': ('real = MCB photograph of an MCB job, homeowner-approved; only these may name a '
                      'town, say "project"/"we built", or appear as our work. illustrative = AI or stock '
                      'imagery and design scenarios; filename and alt must describe the subject only.'),
        'assets': {},
    }
    for base, files in names.items():
        out['assets'][base] = {
            'bucket': 'illustrative',
            'ai_generated': base.startswith('ai-'),
            'reason': REASONS.get(base, DEFAULT_REASON),
            'files': files,
            'used_on': sorted(used.get(base, [])),
        }
    dest = os.path.join(ROOT, 'tools', 'image_provenance.json')
    with open(dest, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    real = [k for k, v in out['assets'].items() if v['bucket'] == 'real']
    print('assets: %d  real: %d  illustrative: %d' % (len(out['assets']), len(real), len(out['assets']) - len(real)))


if __name__ == '__main__':
    main()
