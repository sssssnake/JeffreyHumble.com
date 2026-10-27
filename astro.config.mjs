import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://www.jeffreyhumble.com",
  trailingSlash: "never",
  build: { format: "file" }, // /about -> about.html, matching the old Squarespace URLs
  integrations: [sitemap()],
});
