"""
Package the built Astro homepage as a single self-contained page for the
Artifact viewer: inline every stylesheet, script and image as data: URIs,
and strip the doctype/head/body wrapper the publisher supplies itself.

External hosts are blocked in artifacts except Google Fonts, so anything
else has to travel inside the file.
"""
import re, base64, os, sys, mimetypes, subprocess

DIST = '/home/claude/mcb-astro/dist'
PUB = '/home/claude/mcb-astro/public'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/mcb-astro/artifact.html'
HERO_Q = int(sys.argv[2]) if len(sys.argv) > 2 else 82

html = open(os.path.join(DIST, 'index.html'), encoding='utf-8').read()


def datauri(path, jpeg_quality=None):
    if not os.path.exists(path):
        return None
    if jpeg_quality and path.lower().endswith('.png'):
        jpg = path + '.q%d.jpg' % jpeg_quality
        if not os.path.exists(jpg):
            subprocess.run(['python3', '-c',
                            'from PIL import Image;import sys;'
                            'im=Image.open(sys.argv[1]).convert("RGB");'
                            'im.save(sys.argv[2],"JPEG",quality=int(sys.argv[3]),optimize=True,progressive=True)',
                            path, jpg, str(jpeg_quality)], check=True)
        path = jpg
    mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path, 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode())


# ---- inline stylesheets emitted by the build
def inline_css(m):
    href = m.group(1)
    if href.startswith('http'):
        return m.group(0)                      # Google Fonts stays remote (allowed)
    p = os.path.join(DIST, href.lstrip('/'))
    if not os.path.exists(p):
        return m.group(0)
    return '<style>%s</style>' % open(p, encoding='utf-8').read()

html = re.sub(r'<link[^>]+rel="stylesheet"[^>]*href="([^"]+)"[^>]*>', inline_css, html)
html = re.sub(r'<link[^>]+href="([^"]+)"[^>]*rel="stylesheet"[^>]*>', inline_css, html)

# ---- inline module scripts
def inline_js(m):
    src = m.group(1)
    if src.startswith('http'):
        return m.group(0)
    p = os.path.join(DIST, src.lstrip('/'))
    if not os.path.exists(p):
        return ''
    return '<script type="module">%s</script>' % open(p, encoding='utf-8').read()

html = re.sub(r'<script[^>]*type="module"[^>]*src="([^"]+)"[^>]*></script>', inline_js, html)

# ---- inline every local image reference (src= and inside the hero data-frames JSON)
seen = {}
def sub_img(path):
    if path in seen:
        return seen[path]
    p = os.path.join(PUB, path.lstrip('/'))
    u = datauri(p, HERO_Q if '/hero/' in path else None)
    seen[path] = u or path
    return seen[path]

for path in sorted(set(re.findall(r'(?:src|href)="(/(?:hero|work)/[^"]+)"', html)), key=len, reverse=True):
    html = html.replace('"%s"' % path, '"%s"' % sub_img(path))
for path in sorted(set(re.findall(r'\\?&quot;(/hero/[^&\\"]+)', html)), key=len, reverse=True):
    html = html.replace(path, sub_img(path))
for path in sorted(set(re.findall(r'(/hero/[A-Za-z0-9_.-]+\.png)', html)), key=len, reverse=True):
    html = html.replace(path, sub_img(path))

# ---- strip the wrapper the artifact publisher provides
head = re.search(r'<head[^>]*>(.*?)</head>', html, re.S)
body = re.search(r'<body[^>]*>(.*?)</body>', html, re.S)
head_inner = head.group(1) if head else ''
body_inner = body.group(1) if body else html
# keep title, style and script from head; drop charset/viewport/canonical/og
keep = ''.join(re.findall(r'<title>.*?</title>|<style>.*?</style>|'
                          r'<script(?![^>]*ld\+json).*?</script>|'
                          r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>',
                          head_inner, re.S))
out = keep + body_inner
open(OUT, 'w', encoding='utf-8').write(out)
print('wrote %s  (%.2f MB)' % (OUT, len(out.encode()) / 1e6))
print('images inlined:', len(seen))
