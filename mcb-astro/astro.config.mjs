import { defineConfig } from 'astro/config';
import { buildHomeAssets } from './scripts/hero-assets.mjs';

// Static output only. Every route is crawlable HTML at build time.
// No SSR, no hydration by default — client JS is opt-in per island.
export default defineConfig({
  site: 'https://mcitybuilders.com',
  output: 'static',
  trailingSlash: 'never',
  build: { format: 'directory', inlineStylesheets: 'auto' },
  compressHTML: true,
  vite: { build: { cssCodeSplit: true, assetsInlineLimit: 2048 } },
  integrations: [{
    // Homepage hero frames / room cards / mark: WebP derivatives are generated
    // from the JPGs in public/ before every build. Only writes new *-w1600,
    // *-w800, *-640 and mcb-mark-* files; never touches anything else.
    name: 'mcb-home-assets',
    hooks: {
      'astro:config:setup': async ({ logger }) => { await buildHomeAssets((m) => logger.info(m)); },
    },
  }],
});
