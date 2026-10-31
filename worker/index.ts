/*
  The only server code on the site. Cloudflare serves every page and image as a
  static file; this Worker only runs for /api/* and /blog (see wrangler.jsonc).

  It receives form submissions, drops spam, and posts the rest straight to a
  Discord channel through a Discord webhook.

  Settings (Cloudflare dashboard → this Worker → Settings → Variables and secrets):
    DISCORD_WEBHOOK_URL       (secret)  the webhook URL of the Discord channel
    RESEND_API_KEY            (secret, optional)  with NOTIFY_EMAIL, also emails every submission via Resend
    NOTIFY_EMAIL              (secret, optional)  the address that receives those emails
    FROM_EMAIL                (optional)  sender, e.g. "Site forms <onboarding@resend.dev>"; leave unset to use Resend's test sender, which only reaches the address you signed up with; use your own verified domain for anything else
    ACTIVEPIECES_WEBHOOK_URL  (secret, optional)  also forward each submission to an ActivePieces flow
    TURNSTILE_SECRET_KEY      (secret, optional)  turns on Cloudflare's free bot check
*/

interface Env {
  ASSETS: { fetch: (req: Request) => Promise<Response> };
  DISCORD_WEBHOOK_URL?: string;
  ACTIVEPIECES_WEBHOOK_URL?: string;
  RESEND_API_KEY?: string;
  NOTIFY_EMAIL?: string;
  FROM_EMAIL?: string;
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

  const emailOn = Boolean(env.RESEND_API_KEY && env.NOTIFY_EMAIL);
  if (!env.DISCORD_WEBHOOK_URL && !env.ACTIVEPIECES_WEBHOOK_URL && !emailOn) {
    console.error("No webhook is set; form submission dropped", fields);
    return new Response("Form is not configured", { status: 500 });
  }

  const submittedAt = new Date().toISOString();
  const jobs: Promise<Response>[] = [];

  if (env.DISCORD_WEBHOOK_URL) {
    jobs.push(
      fetch(env.DISCORD_WEBHOOK_URL, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(discordMessage(fields, submittedAt)),
      }),
    );
  }
  if (emailOn) {
    jobs.push(
      fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${env.RESEND_API_KEY}` },
        body: JSON.stringify(emailMessage(fields, env)),
      }),
    );
  }
  if (env.ACTIVEPIECES_WEBHOOK_URL) {
    jobs.push(
      fetch(env.ACTIVEPIECES_WEBHOOK_URL, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ ...fields, submittedAt, site: "jeffreyhumble.com" }),
      }),
    );
  }

  const results = await Promise.allSettled(jobs);
  const delivered = results.some((r) => r.status === "fulfilled" && r.value.ok);
  for (const r of results) {
    if (r.status === "rejected") console.error("Webhook request failed", r.reason);
    else if (!r.value.ok) console.error("Webhook failed", r.value.status, await r.value.text());
  }
  if (!delivered) return new Response("Could not deliver message", { status: 502 });
  return Response.json({ ok: true });
}

// Labels for the fields we know about; any other field is shown under its own name.
const LABELS: Record<string, string> = {
  first_name: "First name",
  last_name: "Last name",
  email: "Email",
  event_date: "Event date",
  budget: "Budget",
};
const SKIP = new Set(["form", "page", "message", "name", "first_name", "last_name", "email"]);

function discordMessage(fields: Record<string, string>, submittedAt: string) {
  const name = [fields.first_name, fields.last_name].filter(Boolean).join(" ") || fields.name || "Someone";
  const clip = (text: string, max: number) => (text.length > max ? text.slice(0, max - 1) + "…" : text);

  const extra = Object.entries(fields)
    .filter(([key, value]) => value && !SKIP.has(key))
    .map(([key, value]) => ({
      name: clip(LABELS[key] ?? key.replace(/[_-]+/g, " "), 256),
      value: clip(value, 1024),
      inline: true,
    }));

  return {
    // No pings, whatever a stranger types into the form.
    allowed_mentions: { parse: [] },
    embeds: [
      {
        title: clip(`${name} sent a message`, 256),
        description: clip(fields.message || "(no message)", 4000),
        color: 0x5865f2,
        fields: [
          { name: "Email", value: clip(fields.email, 1024), inline: true },
          { name: "Form", value: clip(`${fields.form || "unknown"} on ${fields.page || "/"}`, 1024), inline: true },
          ...extra.slice(0, 20),
        ],
        timestamp: submittedAt,
        footer: { text: "jeffreyhumble.com" },
      },
    ],
  };
}

const esc = (t: string) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function emailMessage(fields: Record<string, string>, env: Env) {
  const name = [fields.first_name, fields.last_name].filter(Boolean).join(" ") || fields.name || "Someone";
  const rows = Object.entries(fields)
    .filter(([key, value]) => value && key !== "message")
    .map(([key, value]) => `${LABELS[key] ?? key.replace(/[_-]+/g, " ")}: ${value}`);
  const text = `${fields.message || "(no message)"}\n\n---\n${rows.join("\n")}`;
  return {
    from: env.FROM_EMAIL || "Site forms <onboarding@resend.dev>",
    to: [env.NOTIFY_EMAIL],
    // Hitting reply in your inbox answers the person who wrote in.
    reply_to: fields.email,
    subject: `${name} wrote in on jeffreyhumble.com`,
    text,
    html: `<p style="white-space:pre-wrap">${esc(fields.message || "(no message)")}</p><hr><p style="white-space:pre-wrap;color:#555">${esc(rows.join("\n"))}</p>`,
  };
}
