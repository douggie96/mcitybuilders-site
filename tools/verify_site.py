"""FINAL GATE - run this against the MERGED tree, not against any single branch.

Because the large changes are regenerated rather than merged, nobody will
meaningfully review 150 files of minified HTML. This checklist IS the assurance.

Every number below is a baseline measured on 2026-08-30. If any check FAILS,
stop and report it - do not reconcile the number by editing the baseline.

Usage:  python tools/verify_site.py
Exit code 0 = all pass, 1 = something failed.
"""
import glob
import json
import os
import re
import sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [f for f in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)
         if os.sep + "assets" + os.sep not in f]
INDEXES = [f for f in glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True)
           if os.sep + "assets" + os.sep not in f]

results = []


def check(name, actual, expected, detail=""):
    ok = actual == expected
    results.append((ok, name, actual, expected, detail))
    return ok


def read(f):
    return open(f, encoding="utf-8", errors="replace").read()


# ---- 1. no third-party image hosts -------------------------------------------
for host in ("vibe.filesafe.space", "wsrv.nl", "i.imgur.com"):
    n = sum(read(f).count(host) for f in PAGES)
    check(f"references to {host}", n, 0)

# ---- 2. no broken local image references -------------------------------------
broken = []
for f in PAGES:
    for u in set(re.findall(r'/assets/img/[A-Za-z0-9._-]+', read(f))):
        if not os.path.exists(os.path.join(SITE, u.lstrip("/"))):
            broken.append((os.path.relpath(f, SITE), u))
check("broken local image references", len(broken), 0, str(broken[:3]))

# ---- 3. breadcrumbs -----------------------------------------------------------
trails = 0
mismatch = []
for f in INDEXES:
    h = read(f)
    ld = None
    for m in re.finditer(r'(?is)<script[^>]+ld\+json[^>]*>(.*?)</script>', h):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("@type") == "BreadcrumbList":
            ld = [i["name"] for i in d["itemListElement"]]
    navs = re.findall(r'(?is)<nav class="mcb-breadcrumb".*?</nav>', h)
    if not ld and not navs:
        continue
    if len(navs) != 1:
        mismatch.append((os.path.relpath(f, SITE), f"{len(navs)} trails"))
        continue
    trails += 1
    import html as _h
    vis = [_h.unescape(x) for x in re.findall(r'(?is)>([^<>/]+)</(?:a|span)>', navs[0])
           if x.strip() and x.strip() != "/"]
    if vis != ld:
        mismatch.append((os.path.relpath(f, SITE), "label mismatch"))
check("pages with exactly one breadcrumb trail", trails, 119)
check("breadcrumb label mismatches vs JSON-LD", len(mismatch), 0, str(mismatch[:3]))

# ---- 4. JSON-LD parses everywhere ---------------------------------------------
errs = 0
for f in INDEXES:
    for m in re.finditer(r'(?is)<script[^>]+ld\+json[^>]*>(.*?)</script>', read(f)):
        try:
            json.loads(m.group(1))
        except Exception:
            errs += 1
check("JSON-LD parse errors", errs, 0)
check("pages scanned for JSON-LD", len(INDEXES), 120)

# ---- 5. tag balance -----------------------------------------------------------
unbalanced = []
for f in PAGES:
    h = read(f)
    for t in ("nav", "div", "span", "a", "section", "script", "picture", "li"):
        if len(re.findall(r"<" + t + r"\b", h)) != h.count("</" + t + ">"):
            unbalanced.append((os.path.relpath(f, SITE), t))
check("files with unbalanced tags", len(unbalanced), 0, str(unbalanced[:3]))

# ---- 6. analytics still present ------------------------------------------------
check("files containing gtag(", sum(1 for f in PAGES if "gtag(" in read(f)), 105)
check("files containing fbq(", sum(1 for f in PAGES if "fbq(" in read(f)), 89)

# ---- 7. /contact lead form intact ---------------------------------------------
c = read(os.path.join(SITE, "contact", "index.html"))
check("/contact submitForm handlers", c.count("async function submitForm"), 1)
check("/contact backend.leadconnectorhq refs", c.count("backend.leadconnectorhq.com"), 1)
check("/contact widget refs", c.count("widgets.leadconnectorhq.com") + c.count("chat-widget"), 0)
check("/contact checks res.ok", "ok = res.ok" in c, True)
check("/contact has no empty catch", "catch(err) {}" in c or "catch (err) {}" in c, False)

# ---- 8. dead chat widget fully gone --------------------------------------------
check("widgets.leadconnectorhq.com refs sitewide",
      sum(read(f).count("widgets.leadconnectorhq.com") for f in PAGES), 0)
check("chat-widget refs sitewide",
      sum(read(f).count("chat-widget") for f in PAGES), 0)

# ---- report --------------------------------------------------------------------
print(f"{'':2} {'check':<48} {'actual':>10} {'expected':>10}")
print("-" * 84)
failed = 0
for ok, name, actual, expected, detail in results:
    mark = "OK" if ok else "!!"
    if not ok:
        failed += 1
    print(f"{mark:<2} {name:<48} {str(actual):>10} {str(expected):>10}")
    if not ok and detail:
        print(f"   -> {detail[:120]}")
print("-" * 84)
print(f"{len(results) - failed}/{len(results)} passed")
if failed:
    print("\nFAILED. Stop and report - do not edit the baselines to make this pass.")
sys.exit(1 if failed else 0)
