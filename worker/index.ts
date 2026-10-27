/*
  The only server code on the site. Cloudflare serves every page and image as a
  static file; this Worker only runs for /api/* and /blog (see wrangler.jsonc).

  It receives form submissions, drops spam, and forwards the rest to an
  ActivePieces webhook (which then notifies Discord).

  Settings (Cloudflare dashboard → this Worker → Settings → Variables and secrets):
    ACTIVEPIECES_WEBHOOK_URL  (secret)  the "Catch Webhook" URL of your ActivePieces flow
    TURNSTILE_SECRET_KEY      (secret, optional)  turns on Cloudflare's free bot check
*/

interface Env {
  ASSETS: { fetch: (req: Request) => Promise<Response> };
  ACTIVEPIECES_WEBHOOK_URL?: string;
  TURNSTILE_SECRET_KEY?: string;
}

const MAX_FIELD = 5000;

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Squarespace's RSS feed lived at /blog?format=rss; keep old feed subscribers working.
    if (url.pathname === "/blog" && url.searchParams.get("format") === "rss") {
      return Response.redirect(new URL("/blog/rss.xml", url).href, 301);
    }

    if (url.pathname === "/api/form") {
      if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
      return handleForm(request, env);
    }

    return env.ASSETS.fetch(request);
  },
};

async function handleForm(request: Request, env: Env): Promise<Response> {
  let body: Record<string, unknown>;
  try {
    body = await request.json();
  } catch {
    return new Response("Bad request", { status: 400 });
  }

  // Honeypot: real visitors never fill this in. Pretend it worked so bots move on.
  if (typeof body.website === "string" && body.website.trim() !== "") {
    return Response.json({ ok: true });
  }

  if (env.TURNSTILE_SECRET_KEY) {
    const token = String(body["cf-turnstile-response"] ?? "");
    const check = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      body: new URLSearchParams({
        secret: env.TURNSTILE_SECRET_KEY,
        response: token,
        remoteip: request.headers.get("cf-connecting-ip") ?? "",
      }),
    }).then((r) => r.json() as Promise<{ success: boolean }>);
    if (!check.success) return new Response("Verification failed", { status: 400 });
  }

  const email = String(body.email ?? "").trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return new Response("A valid email is required", { status: 400 });
  }

  // Keep only plain text fields, trimmed and size-limited.
  const fields: Record<string, string> = {};
  for (const [key, value] of Object.entries(body)) {
    if (key === "website" || key === "cf-turnstile-response") continue;
    if (typeof value !== "string") continue;
    fields[key] = value.trim().slice(0, MAX_FIELD);
  }

  if (!env.ACTIVEPIECES_WEBHOOK_URL) {
    console.error("ACTIVEPIECES_WEBHOOK_URL is not set; form submission dropped", fields);
    return new Response("Form is not configured", { status: 500 });
  }

  const res = await fetch(env.ACTIVEPIECES_WEBHOOK_URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ ...fields, submittedAt: new Date().toISOString(), site: "jeffreyhumble.com" }),
  });
  if (!res.ok) {
    console.error("ActivePieces webhook failed", res.status, await res.text());
    return new Response("Could not deliver message", { status: 502 });
  }
  return Response.json({ ok: true });
}
