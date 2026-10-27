// /llms.txt: a plain-text map of the site for AI assistants (https://llmstxt.org)
import { getPublishedPosts, postPath } from "../lib/posts";
import { site } from "../data/site";

export async function GET() {
  const posts = await getPublishedPosts();
  const lines = [
    `# ${site.name}`,
    "",
    `> ${site.description}. Founder of the Fountain Institute; writes about product strategy, design, innovation and AI.`,
    "",
    "## Pages",
    `- [About](${site.url}/about): background, experience and approach`,
    `- [Consulting Services](${site.url}/services): strategy consulting, innovation experiments, corporate workshops`,
    `- [Speaking & Workshop Requests](${site.url}/speaking-requests): talks and workshops`,
    `- [Free Resources](${site.url}/resources): templates and recorded talks`,
    `- [Portfolio](${site.url}/portfolio): selected projects`,
    `- [CV](${site.url}/curriculum-vitae)`,
    "",
    "## Blog posts",
    ...posts.map((p) => `- [${p.data.title}](${site.url}${postPath(p)})${p.data.excerpt ? `: ${p.data.excerpt}` : ""}`),
    "",
  ];
  return new Response(lines.join("\n"), { headers: { "content-type": "text/plain; charset=utf-8" } });
}
