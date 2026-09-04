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
check("pages with exactly one breadcrumb trail", trails, 122)  # 2026-09-01: +3 pages (/terms, /accessibility, /cookie-policy)
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
check("pages scanned for JSON-LD", len(INDEXES), 123)  # 2026-09-01: +3 pages (/terms, /accessibility, /cookie-policy)

# ---- 5. tag balance -----------------------------------------------------------
unbalanced = []
for f in PAGES:
    h = read(f)
    for t in ("nav", "div", "span", "a", "section", "script", "picture", "li"):
        if len(re.findall(r"<" + t + r"\b", h)) != h.count("</" + t + ">"):
            unbalanced.append((os.path.relpath(f, SITE), t))
check("files with unbalanced tags", len(unbalanced), 0, str(unbalanced[:3]))

# ---- 6. analytics still present ------------------------------------------------
check("files containing gtag(", sum(1 for f in PAGES if "gtag(" in read(f)), 123)  # 2026-09-01: +3 pages (/terms, /accessibility, /cookie-policy)
check("files containing fbq(", sum(1 for f in PAGES if "fbq(" in read(f)), 92)  # 2026-09-01: +3 pages (/terms, /accessibility, /cookie-policy)

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

# ---- 9. claims compliance (added 2026-09-03, Day 72) ---------------------------
# An image or a sentence may not present AI/stock imagery or an invented job as
# Maverick City Builders' completed work. See
# 09 - Daily Logs & Plans/audits/MCB_IMAGE_AND_CLAIMS_COMPLIANCE_AUDIT_2026-09-03.md
# All expected values are 0 by construction, not by measurement -- any nonzero
# result is a real regression. Do not raise these baselines.

DISCLOSURE = ("Some images on this site are design illustrations, including AI-generated "
              "concepts, and are not photographs of Maverick City Builders projects. "
              "Photos of our own work are labelled as such.")

SERVICE_TOWNS = ("Lancaster", "Sterling", "Clinton", "Bolton", "Hudson", "Berlin", "Harvard",
                 "Worcester", "Leominster", "Fitchburg", "Marlborough", "Stow", "Boxborough",
                 "Acton", "Concord", "Sudbury", "Littleton", "West Sterling")

check("pages containing 'Project Examples'",
      sum(1 for f in PAGES if "Project Examples" in read(f)), 0,
      str([os.path.relpath(f, SITE) for f in PAGES if "Project Examples" in read(f)][:3]))

TIME_CLAIM = re.compile(r"We (completed|built|finished|remodeled|renovated)"
                        r"[^.]{0,60}(this spring|this summer|last year|this year)")
tc = [os.path.relpath(f, SITE) for f in PAGES if TIME_CLAIM.search(read(f))]
check("pages claiming a recent completed job", len(tc), 0, str(tc[:3]))

check("pages containing 'Real homes, real transformations'",
      sum(1 for f in PAGES if "Real homes, real transformations" in read(f)), 0)

check("pages missing the image disclosure line",
      sum(1 for f in PAGES if DISCLOSURE not in read(f)), 0,
      str([os.path.relpath(f, SITE) for f in PAGES if DISCLOSURE not in read(f)][:3]))

# provenance-driven image checks
PROV = os.path.join(SITE, "tools", "image_provenance.json")
prov = json.load(open(PROV, encoding="utf-8"))["assets"] if os.path.exists(PROV) else {}
REAL = {k for k, v in prov.items() if v.get("bucket") == "real"}
check("image_provenance.json present", os.path.exists(PROV), True)

VARIANT = re.compile(r"-(480|800|1408|768|1200)\.(webp|jpg)$|\.(jpg|jpeg|webp|png)$")
BANNED = tuple(t.lower() for t in SERVICE_TOWNS) + (
    "worcester county", "central ma", "project", "remodel in", "renovation in",
    "repaint in", "we built", "our work")

bad_placements = []
for f in PAGES:
    for tag in re.findall(r"<img\b[^>]*>", read(f)):
        m_src = re.search(r'src="([^"]*)"', tag)
        if not m_src or "/assets/img/" not in m_src.group(1):
            continue
        base = VARIANT.sub("", os.path.basename(m_src.group(1)))
        if base in REAL:
            continue  # real MCB job photos may name a town
        m_alt = re.search(r'alt="([^"]*)"', tag)
        alt = (m_alt.group(1) if m_alt else "").lower()
        # A blog header may use its article title as alt -- that describes the
        # article, not a job -- so alt is exempt there. The filename rule is not.
        if (os.sep + "blog" + os.sep) in f:
            alt = ""
        hay = base.replace("-", " ").lower()
        for word in BANNED:
            if word in hay or word in alt:
                bad_placements.append((os.path.relpath(f, SITE), base, word))
                break
check("illustrative image placements claiming a town or project",
      len(bad_placements), 0, str(bad_placements[:3]))

IMGDIR = os.path.join(SITE, "assets", "img")
bad_names = []
if os.path.isdir(IMGDIR):
    for p in sorted(os.listdir(IMGDIR)):
        base = VARIANT.sub("", p)
        if base in REAL:
            continue
        if "-project-in-" in base or re.search(r"-in-[a-z-]+-ma$", base):
            bad_names.append(p)
check("illustrative asset filenames claiming a town or project", len(bad_names), 0, str(bad_names[:3]))

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
