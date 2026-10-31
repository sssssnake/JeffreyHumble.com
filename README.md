# jeffreyhumble.com

Jeff Humble's personal site, moved off Squarespace in October 2026. It's a static
site built with [Astro](https://astro.build), hosted on Cloudflare, with all content
as plain files in this repo.

## Where things live

| What | Where |
| --- | --- |
| Blog posts | `src/content/blog/*.md`, one Markdown file per post (file name = URL) |
| Pages (home, about, services…) | `src/pages/*.astro` |
| Navigation, social links, footer links | `src/data/site.ts` |
| Colors, fonts, type sizes | `src/styles/global.css` (tokens at the top) |
| Images | `public/images/` |
| Form handling | `worker/index.ts` |
| Old-URL redirects | `public/_redirects` |

## Editing

- **Write a new post:** add `src/content/blog/my-new-post.md` with a `title`, `date`
  and (optionally) `excerpt` and `image` at the top. Copy any existing post as a template.
  Set `draft: true` to keep it unpublished.
- **Change text on a page:** open the page in `src/pages/` and edit the words. The
  `<Section>` / `<Block>` wrappers place things on the same grid Squarespace used
  (`d` = desktop position, `m` = phone position); you can ignore them when editing text.
- Or just ask Claude: "change the headline on the about page to …".

Every push to `main` on GitHub rebuilds and publishes the site in about a minute.

## Running it locally

```
npm install
npm run dev        # http://localhost:4321
npm run build      # builds into dist/
npx wrangler dev   # runs the built site on Cloudflare's runtime, including the form handler
```

## Forms

Forms post to `/api/form`. The worker drops spam and posts submissions straight
to a Discord channel. Set these in the Cloudflare dashboard (Worker → Settings →
Variables and secrets):

- `DISCORD_WEBHOOK_URL`: the webhook URL of the Discord channel
- `RESEND_API_KEY` and `NOTIFY_EMAIL` (optional): also email each submission through
  Resend; `FROM_EMAIL` (optional) sets the sender and must be on a domain verified in Resend
- `ACTIVEPIECES_WEBHOOK_URL` (optional): also forward each submission to an
  ActivePieces flow
- `TURNSTILE_SECRET_KEY` (optional) plus `PUBLIC_TURNSTILE_SITE_KEY` as a build
  variable, to add Cloudflare's free bot check

## Migration tools

`tools/` holds the one-time scripts that converted the Squarespace export and
saved pages. They're kept for the Fountain Institute migration; the site
doesn't use them.
