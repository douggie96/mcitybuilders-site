#!/usr/bin/env python3
"""Idempotent accessibility patch for the older static (non-Astro) pages. Run by DEPLOY.bat.

For every index.html under the site root that is NOT an Astro-published page:
  (a) Skip link. Inserts <a class="mcb-skip" href="#main">Skip to content</a> as the first
      child of <body>, plus a <style id="mcb-a11y"> block in <head> that hides the link until
      it receives keyboard focus. The link must point at a real element: the page's <main>
      (id="main" is added when it has none). Pages with no <main> get id="main" on the first
      <section>/<article>/<div> that encloses the first <h1>. If that also fails, the skip
      link is not added and the page is logged as a SKIP with the reason.
  (b) 44px hamburger target. The same style block gives button[aria-label="Open menu"] and
      button[aria-label="Close menu"] a 44x44 minimum hit area.

Conservative by design: a page is only touched when the exact markup expected is present
(exactly one <head>...</head>, exactly one <body ...> tag). Running it twice changes nothing
on the second run. Exit code is 0 unless a file it tried to write could not be written.

Usage:  python patch_static.py            (ROOT = parent folder of this script)
        python patch_static.py <ROOT>     (explicit site root, used for testing)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'mcb-astro', 'node_modules', 'tools', '_cdn_dl', '_cdn_dl2', '.vercel'}
MANIFEST = os.path.join(ROOT, 'mcb-astro', 'published-manifest.json')

STYLE_ID = 'mcb-a11y'
STYLE_BLOCK = (
    '<style id="' + STYLE_ID + '">'
    '.mcb-skip{position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden}'
    '.mcb-skip:focus{position:fixed;left:16px;top:16px;width:auto;height:auto;overflow:visible;'
    'z-index:100000;background:#E10600;color:#fff;padding:12px 16px;font-weight:700;'
    'text-decoration:none;outline:2px solid #fff;outline-offset:2px}'
    'button[aria-label="Open menu"],button[aria-label="Close menu"]'
    '{min-width:44px;min-height:44px;display:inline-flex;align-items:center;justify-content:center}'
    '</style>'
)
SKIP_LINK_TMPL = '<a class="mcb-skip" href="#%s">Skip to content</a>'

RE_HEAD_CLOSE = re.compile(r'</head\s*>', re.I)
RE_BODY_OPEN = re.compile(r'<body\b[^>]*>', re.I)
RE_MAIN_OPEN = re.compile(r'<main\b[^>]*>', re.I)
RE_H1_OPEN = re.compile(r'<h1\b', re.I)
RE_CONTAINER = re.compile(r'<(/?)(section|article|div)\b[^>]*>', re.I)
RE_ID_ATTR = re.compile(r'\sid\s*=\s*("([^"]*)"|\'([^\']*)\')', re.I)
RE_MENU_BTN = re.compile(r'<button\b[^>]*aria-label\s*=\s*"([^"]*[Mm]enu[^"]*)"[^>]*>')


def norm(p):
    return p.replace('\\', '/')


def load_manifest():
    """Set of site-relative paths (forward slashes) that are Astro-published pages."""
    files = set()
    try:
        with open(MANIFEST, encoding='utf8') as fh:
            data = json.load(fh)
    except (OSError, ValueError) as e:
        print('patch_static: WARNING cannot read %s (%s); no Astro pages will be excluded by manifest' % (MANIFEST, e))
        return files
    entries = data.get('files', data) if isinstance(data, dict) else data
    for entry in entries or []:
        if isinstance(entry, str):
            e = norm(entry).strip('/')
            files.add(e)
            if e.endswith('/index.html'):
                files.add(e[:-len('/index.html')])
    return files


def tag_id(open_tag):
    m = RE_ID_ATTR.search(open_tag)
    if not m:
        return None
    return m.group(2) if m.group(2) is not None else m.group(3)


def add_id(open_tag, new_id):
    """Insert id="new_id" right after the tag name of an opening tag."""
    m = re.match(r'<([a-zA-Z][a-zA-Z0-9]*)', open_tag)
    name = m.group(1)
    return '<' + name + ' id="' + new_id + '"' + open_tag[len(name) + 1:]


def find_target(html):
    """Return (html, target_id, note) or (html, None, reason)."""
    m = RE_MAIN_OPEN.search(html)
    if m:
        existing = tag_id(m.group(0))
        if existing:
            return html, existing, 'main already has id="%s"' % existing
        if re.search(r'\sid\s*=\s*["\']main["\']', html, re.I):
            return html, None, 'main has no id and id="main" is already used by another element'
        new_tag = add_id(m.group(0), 'main')
        return html[:m.start()] + new_tag + html[m.end():], 'main', 'added id="main" to <main>'
    # No <main>: find the container that encloses the first <h1>.
    h1 = RE_H1_OPEN.search(html)
    if not h1:
        return html, None, 'no <main> and no <h1>'
    body = RE_BODY_OPEN.search(html)
    start = body.end() if body else 0
    stack = []  # (match_start, match_end, open_tag)
    for t in RE_CONTAINER.finditer(html, start, h1.start()):
        if t.group(1):
            if stack:
                stack.pop()
        else:
            stack.append((t.start(), t.end(), t.group(0)))
    if not stack:
        return html, None, 'no <main> and first <h1> has no enclosing section/article/div'
    s, e, open_tag = stack[-1]
    existing = tag_id(open_tag)
    if existing:
        return html, existing, 'no <main>; h1 container already has id="%s"' % existing
    if re.search(r'\sid\s*=\s*["\']main["\']', html, re.I):
        return html, None, 'no <main>; id="main" is already used by another element'
    new_tag = add_id(open_tag, 'main')
    return html[:s] + new_tag + html[e:], 'main', 'added id="main" to <%s> enclosing first <h1>' % re.match(r'<(\w+)', open_tag).group(1)


def patch_page(html):
    """Return (new_html, status, notes). status in {'patched','already','skip'}."""
    notes = []
    heads = RE_HEAD_CLOSE.findall(html)
    bodies = list(RE_BODY_OPEN.finditer(html))
    if len(heads) != 1:
        return html, 'skip', ['expected exactly one </head>, found %d' % len(heads)]
    if len(bodies) != 1:
        return html, 'skip', ['expected exactly one <body> tag, found %d' % len(bodies)]

    has_style = ('id="' + STYLE_ID + '"') in html
    has_link = 'class="mcb-skip"' in html

    # Hamburger diagnostics (the CSS is selector-based; here we only report what the page has).
    labels = RE_MENU_BTN.findall(html)
    known = [l for l in labels if l in ('Open menu', 'Close menu')]
    other = [l for l in labels if l not in ('Open menu', 'Close menu')]
    if known:
        notes.append('hamburger selector matches: %s' % ', '.join(sorted(set(known))))
    elif other:
        notes.append('HAMBURGER MISMATCH: no "Open menu"/"Close menu" button; menu buttons found use: %s' % ', '.join(sorted(set(other))))
    else:
        notes.append('no hamburger on this page (nav is plain links, nothing to enlarge)')

    out = html
    changed = False

    # A page can be regenerated by another tool that keeps the skip link but drops the id it
    # points at. Treat a skip link whose target no longer exists as unpatched and repair it.
    if has_link:
        lm = re.search(r'<a class="mcb-skip" href="#([^"]+)">Skip to content</a>', out)
        if lm and not re.search(r'\sid\s*=\s*["\']' + re.escape(lm.group(1)) + r'["\']', out):
            out2, target, why = find_target(out)
            if target is None:
                notes.append('SKIP skip link repair: link points at #%s which no longer exists; %s' % (lm.group(1), why))
                return html, 'skip', notes
            out = out2
            if target != lm.group(1):
                out = out.replace(lm.group(0), SKIP_LINK_TMPL % target, 1)
            changed = True
            notes.append('repaired skip link target -> #%s (%s)' % (target, why))

    if has_style and has_link and not changed:
        return html, 'already', notes

    if not has_style:
        m = RE_HEAD_CLOSE.search(out)
        out = out[:m.start()] + STYLE_BLOCK + out[m.start():]
        changed = True
        notes.append('added #%s style block' % STYLE_ID)

    if not has_link:
        out2, target, why = find_target(out)
        if target is None:
            notes.append('SKIP skip link: ' + why)
            if not changed:
                return html, 'skip', notes
        else:
            out = out2
            b = RE_BODY_OPEN.search(out)
            out = out[:b.end()] + (SKIP_LINK_TMPL % target) + out[b.end():]
            changed = True
            notes.append('added skip link -> #%s (%s)' % (target, why))

    return out, ('patched' if changed else 'already'), notes


def main():
    astro = load_manifest()
    scanned = patched = already = 0
    skipped = []
    write_failed = []
    excluded = 0
    infos = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = sorted(d for d in dns if d not in SKIP_DIRS)
        for fn in sorted(fns):
            if fn.lower() != 'index.html':
                continue
            p = os.path.join(dp, fn)
            rel = norm(os.path.relpath(p, ROOT))
            reldir = rel[:-len('/index.html')] if '/' in rel else ''
            if rel in astro or (reldir and reldir in astro):
                excluded += 1
                continue
            try:
                with open(p, encoding='utf8', newline='') as fh:
                    html = fh.read()
            except (OSError, UnicodeDecodeError) as e:
                skipped.append((rel, 'cannot read: %s' % e))
                continue
            if 'data-astro-cid' in html:
                # Astro build output not listed in the manifest: never a static-template page.
                skipped.append((rel, 'Astro build output (data-astro-cid) not in manifest'))
                continue
            scanned += 1
            new_html, status, notes = patch_page(html)
            if status == 'skip':
                skipped.append((rel, '; '.join(notes)))
                continue
            if status == 'already':
                already += 1
                infos.append((rel, 'already patched; ' + '; '.join(notes)))
                continue
            try:
                with open(p, 'w', encoding='utf8', newline='') as fh:
                    fh.write(new_html)
            except OSError as e:
                write_failed.append((rel, str(e)))
                continue
            patched += 1
            infos.append((rel, '; '.join(notes)))
            if any(n.startswith('SKIP skip link') for n in notes):
                skipped.append((rel, [n for n in notes if n.startswith('SKIP')][0]))

    for rel, note in infos:
        print('  ' + rel + ': ' + note)
    print('patch_static: root=%s' % ROOT)
    print('patch_static: %d page(s) scanned, %d patched, %d already patched, %d skipped, %d Astro page(s) excluded by manifest'
          % (scanned, patched, already, len(skipped), excluded))
    for rel, why in skipped:
        print('  SKIP ' + rel + ': ' + why)
    for rel, why in write_failed:
        print('  FAIL write ' + rel + ': ' + why)
    sys.exit(1 if write_failed else 0)


if __name__ == '__main__':
    main()
