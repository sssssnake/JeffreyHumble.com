import rss from "@astrojs/rss";
import { getPublishedPosts, postPath } from "../../lib/posts";

export async function GET(context: { site: URL }) {
  const posts = await getPublishedPosts();
  return rss({
    title: "Jeff Humble's Blog",
    description: "Writing on product strategy, design, innovation and AI.",
    site: context.site,
    items: posts.map((p) => ({ title: p.data.title, pubDate: p.data.date, description: p.data.excerpt, link: postPath(p) })),
  });
}
