import { defineConfig } from 'astro/config';

// Static output only. Every route is crawlable HTML at build time.
// No SSR, no hydration by default — client JS is opt-in per island.
export default defineConfig({
  site: 'https://mcitybuilders.com',
  output: 'static',
  trailingSlash: 'never',
  build: { format: 'directory', inlineStylesheets: 'auto' },
  compressHTML: true,
  vite: { build: { cssCodeSplit: true, assetsInlineLimit: 2048 } },
});
