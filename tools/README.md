# tools/ — regeneration and verification scripts

These are **not** part of the deployed site. `.vercelignore` excludes `tools/` and
`*.py` so nothing here is served publicly. Confirm that after the first deploy:
`curl -I https://mcitybuilders.com/tools/verify_site.py` must return **404**.

---

## ⚠️ Standing constraint: this repo's HTML is minified

Every page is a handful of very long lines — the whole `<head>` is typically one
line. Git diffs at **line** granularity, so **any two branches that touch the same
page will conflict**, even when the edits are in completely unrelated places.

This is not a bug to fix. **Do NOT un-minify** to work around it — that is a
120-file rewrite with its own risk and no user-visible benefit.

**Instead: regenerate, don't merge.** The large sitewide changes are produced by
deterministic scripts. When a script-generated branch conflicts with a merged
tree, discard its HTML changes and re-run the script on the merged result. Both
scripts are idempotent and safe to re-run.

Measured 2026-08-30 — `fix/image-migration` conflicted with four other branches
(147, 32, 17 and 12 files). Regenerating took two script runs; resolving would
have meant hand-editing ~150 files of minified HTML.

---

## Scripts, in the order they must run

### 1. `image_migrate_rewrite.py`
Rewrites every image reference to the local `/assets/img/` copies:
`<img>` → `<picture>` with a WebP `<source>` and a JPEG/PNG fallback, favicon,
`og:image` / `twitter:image`, `preload` hints, and CSS `background-image` URLs.

Requires `_phase2_manifest.json` and `_cdn_assets.txt` (kept in `MCB/`, outside
this repo — the 44.6 MB of raw originals must never enter git history).

**Run before the breadcrumb script**, because it rewrites `<img>` tags that the
breadcrumb trail sits next to.

### 2. `breadcrumb_render.py`
Renders the visible breadcrumb trail under the header on every page except the
homepage. Labels are read from **that page's own `BreadcrumbList` JSON-LD**, so
the visible trail and the structured data cannot drift apart.

Handles both header shapes on this site: most pages use `<header>`; the
`areas-we-serve/*` pages use a bare `<nav>` with no `<header>`.

Ends with a **completeness gate** — it raises `SystemExit` unless it rendered a
trail on every page but the homepage. A script that reports success on a partial
run is the same class of bug as a form reporting success on a failed POST; the
first version of this script cheerfully printed "105 pages" while silently
skipping 14.

### 3. `verify_site.py` — THE FINAL GATE
Run against the **merged tree**, not any single branch. Because the big changes
are regenerated rather than reviewed, this checklist is the assurance.

Baselines measured 2026-08-30:

| Check | Expected |
|---|---|
| refs to `vibe.filesafe.space` / `wsrv.nl` / `i.imgur.com` | 0 |
| broken local image references | 0 |
| pages with exactly one breadcrumb trail | 119 |
| breadcrumb label mismatches vs JSON-LD | 0 |
| JSON-LD parse errors | 0 |
| pages scanned | 120 |
| files with unbalanced tags | 0 |
| files containing `gtag(` | 105 |
| files containing `fbq(` | 89 |
| `/contact` `submitForm` handlers | 1 |
| `/contact` `backend.leadconnectorhq.com` refs | 1 |
| `/contact` widget refs | 0 |
| `widgets.leadconnectorhq.com` refs sitewide | 0 |
| `chat-widget` refs sitewide | 0 |

**If a number differs, stop and report it. Do not edit the baseline to make the
check pass.**

---

## Merge / regenerate procedure

```bash
git tag pre-merge-2026-08-30 main      # rollback point — do this FIRST

# merge the nine small branches in order (verified clean, 36/36 pairs tested)
#   1 fix/contact-form-error-handling
#   2 chore/remove-dead-chat-widget      (after 1 — it touches /contact)
#   3 fix/www-canonical-redirect
#   4 fix/services-legacy-redirects      (rebased onto 3 — both edit vercel.json)
#   5 fix/municipal-addresses
#   6 fix/portfolio-duplicate-photo
#   7 fix/blog-index-missing-posts
#   8 fix/second-contextual-links
#   9 fix/schema-phase3

# then REGENERATE rather than merge the two large branches:
python tools/image_migrate_rewrite.py
python tools/breadcrumb_render.py
python tools/verify_site.py             # must exit 0
```

`assets/img/` is already built and committed on `fix/image-migration`; only the
reference rewrite needs re-running.

---

## Bulk-edit safety practice

Every bulk edit must answer: **what did this touch that it should not have?**

Two real incidents on 2026-08-30, both caught by post-run checks and neither by
the edit itself:

- `rm -rf assets/img` deleted **16 tracked local WebP files** the inventory had
  missed (`hero.webp`, 33 refs; `logo.webp`, 30 refs). Restored from HEAD.
- A "remove everything containing `leadconnectorhq`" filter deleted the
  `/contact` **lead form handler**, because it POSTs to
  `backend.leadconnectorhq.com`. Restored and redone with an explicit guard.

So: run the check, and record it in the commit message.
