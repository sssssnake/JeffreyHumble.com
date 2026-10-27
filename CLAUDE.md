# Notes for AI assistants working on this site

- Astro static site, deployed to Cloudflare Workers static assets via `wrangler.jsonc`.
  Build: `npm run build` (output `dist/`). Only dynamic code: `worker/index.ts`.
- URLs must stay exactly as they are (they match the old Squarespace site for SEO).
  `build.format: "file"` and `trailingSlash: "never"` are deliberate. If a page or post
  URL changes, add a 301 to `public/_redirects`.
- Blog posts: Markdown in `src/content/blog/`, schema in `src/content.config.ts`.
  Small HTML snippets inside posts (centred captions, galleries, videos) are intentional.
- Pages use `<Section>` + `<Block>` (src/components) to reproduce Squarespace's grid:
  `m`/`d` are `row-start/col-start/row-end/col-end` on an 8-col (phone) / 24-col
  (desktop) grid plus a gutter column each side. Text lives in `.rich` divs.
- Design tokens are CSS variables at the top of `src/styles/global.css`.
- Jeff's writing style: plain, direct, no em dashes.
