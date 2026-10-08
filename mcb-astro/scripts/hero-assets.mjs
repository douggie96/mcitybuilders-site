import { fileURLToPath } from 'node:url';
/**
 * Homepage asset pipeline (cinematic homepage, Phase 2).
 * Generates WebP derivatives next to their sources in public/. Idempotent:
 * an output is only (re)written when it is missing or older than its source.
 * Never touches an existing file it did not generate (the older hand-made
 * *-800 / *-1400 webps in public/rooms are left alone).
 *
 * Run standalone:  node scripts/hero-assets.mjs
 * Also runs automatically at the start of every `astro build` (see astro.config.mjs),
 * so a K0_dated.jpg dropped into public/hero/ gets its WebPs on the next build.
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PUB = path.join(ROOT, 'public');

const stale = (src, out) =>
  !fs.existsSync(out) || fs.statSync(out).mtimeMs < fs.statSync(src).mtimeMs;

export async function buildHomeAssets(log = console.log) {
  let sharp;
  try { sharp = (await import('sharp')).default; }
  catch { log('[hero-assets] sharp not installed - skipping WebP generation'); return; }

  const jobs = [];
  // 1. Hero frames: K<n>_<name>.jpg -> -w1600.webp and -w800.webp (the -w prefix keeps clear of older hand-made files)
  const heroDir = path.join(PUB, 'hero');
  for (const f of fs.readdirSync(heroDir)) {
    if (!/^K\d_[a-z]+\.jpg$/i.test(f)) continue;
    const src = path.join(heroDir, f), base = f.replace(/\.jpg$/i, '');
    for (const w of [1600, 800]) jobs.push({ src, out: path.join(heroDir, `${base}-w${w}.webp`), w, q: w > 1000 ? 74 : 70 });
  }
  // 2. Room cards: every rooms/*.jpg -> -640.webp (cards render at <=420 css px)
  const roomDir = path.join(PUB, 'rooms');
  for (const f of fs.readdirSync(roomDir)) {
    if (!/\.jpg$/i.test(f)) continue;
    const src = path.join(roomDir, f);
    jobs.push({ src, out: path.join(roomDir, f.replace(/\.jpg$/i, '-640.webp')), w: 640, q: 70 });
  }
  // Kitchen card reuses the finished hero frame at card size.
  jobs.push({ src: path.join(heroDir, 'K4_finished.jpg'), out: path.join(roomDir, 'kitchen-640.webp'), w: 640, q: 70 });
  // 3. The mark on dark: Doug's own transparent logo (01 - Brand & Logos/
  //    MCB_logo_transparent.png, kept in assets-src/ so the 630 KB source is not deployed). Trimmed to its alpha
  //    bounding box, resized, WebP with alpha. No filtering, no softening.
  const mark = path.join(ROOT, 'assets-src', 'mcb-logo-transparent.png');   // source only - not shipped
  for (const w of [696, 480, 240]) jobs.push({ src: mark, out: path.join(PUB, 'brand', `mcb-mark-${w}.webp`), w, q: 82, alpha: true, trim: true });

  let made = 0;
  for (const j of jobs) {
    if (!fs.existsSync(j.src) || !stale(j.src, j.out)) continue;
    await (j.trim ? sharp(j.src).trim({ threshold: 0 }) : sharp(j.src)).resize({ width: j.w, withoutEnlargement: true })
      .webp({ quality: j.q, alphaQuality: j.alpha ? 80 : undefined, effort: 5 })
      .toFile(j.out);
    made++;
  }
  log(`[hero-assets] ${made} WebP file(s) written, ${jobs.length - made} up to date`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) {
  await buildHomeAssets();
}
