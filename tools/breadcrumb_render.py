"""Render a visible breadcrumb trail on every page.

Labels are read from that page's OWN BreadcrumbList JSON-LD, so the visible
trail and the structured data can never diverge.

Idempotent: re-running strips any previously rendered trail before inserting,
so this can be re-run on a merged tree instead of resolving merge conflicts.

Usage:  python _breadcrumb_render.py
"""
import re
import glob
import json
import io
import html
import os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

added = 0
skipped = []

for f in sorted(glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True)):
    if os.sep + "assets" + os.sep in f:
        continue
    rel = os.path.relpath(f, SITE).replace(os.sep, "/")
    s = io.open(f, encoding="utf-8", newline="").read()

    # strip any previously rendered trail first, so this stays idempotent
    s = re.sub(r'(?is)<nav class="mcb-breadcrumb".*?</nav>', "", s)

    crumbs = None
    for m in re.finditer(r'(?is)<script[^>]+ld\+json[^>]*>(.*?)</script>', s):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("@type") == "BreadcrumbList":
            crumbs = [(i["name"], i["item"]) for i in d["itemListElement"]]

    if not crumbs or len(crumbs) < 2:
        skipped.append((rel, "no BreadcrumbList (expected on the homepage)"))
        continue

    # anchor: after </header>, or after the top nav's </nav> on pages that use
    # a bare <nav> instead of <header>
    anchor = re.search(r'(?is)</header>', s)
    if not anchor:
        body = re.search(r'(?is)<body[^>]*>', s)
        if body:
            anchor = re.compile(r'(?is)</nav>').search(s, body.end())
    if not anchor:
        skipped.append((rel, "no </header> or </nav> anchor"))
        continue

    parts = []
    for i, (name, url) in enumerate(crumbs):
        label = html.escape(name)
        if i == len(crumbs) - 1:
            parts.append(f'<span aria-current="page" style="color:#C0C0C0;">{label}</span>')
        else:
            path = url.replace("https://mcitybuilders.com", "") or "/"
            parts.append(f'<a href="{path}" style="color:#8A8A8A;text-decoration:none;">{label}</a>')

    sep = '<span aria-hidden="true" style="color:#444;margin:0 8px;">/</span>'
    trail = (
        '<nav class="mcb-breadcrumb" aria-label="Breadcrumb" '
        'style="background:#000;border-bottom:1px solid #1a1a1a;padding:12px 24px;'
        'font-size:0.8rem;font-family:Montserrat,sans-serif;">'
        '<div style="max-width:1200px;margin:0 auto;overflow-x:auto;white-space:nowrap;">'
        + sep.join(parts) +
        '</div></nav>'
    )

    s = s[:anchor.end()] + trail + s[anchor.end():]
    io.open(f, "w", encoding="utf-8", newline="").write(s)
    added += 1

print(f"visible breadcrumb rendered on {added} pages")
print(f"skipped {len(skipped)}:")
for rel, why in skipped:
    print(f"   {rel}  -  {why}")

# PARITY / COMPLETENESS GATE - a script that reports success on a partial run is
# the same class of bug as a form reporting success on a failed POST.
expected = len([f for f in glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True)
                if os.sep + "assets" + os.sep not in f]) - 1   # homepage has no trail
if added != expected:
    raise SystemExit(f"FAILED: rendered {added} trails, expected {expected}. "
                     f"Skipped: {skipped}")
print(f"OK: {added}/{expected} pages rendered (homepage correctly excluded)")
