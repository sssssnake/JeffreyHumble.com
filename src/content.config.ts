import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

// Blog posts live in src/content/blog as Markdown files.
// The file name is the URL: vision-vs-strategy.md -> /blog/vision-vs-strategy
const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    excerpt: z.string().optional(),
    seoTitle: z.string().optional(), // browser tab / Google title, if different from the title
    seoDescription: z.string().optional(), // Google snippet, if different from the excerpt
    image: z.string().optional(), // shown in the blog list and when shared
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false), // drafts are never published
    path: z.string().optional(), // only for posts whose old URL doesn't match the file name
  }),
});

export const collections = { blog };
