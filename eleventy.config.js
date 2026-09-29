const sass = require("sass");
const path = require("node:path");

require("dotenv").config();

/**
 * Eleventy replaces Vue CLI + webpack. Output is plain HTML and CSS; no runtime
 * framework ships. See #501 for the rewrite plan.
 */
module.exports = function eleventyConfig(config) {
  // Dates in the data are date-only ISO strings; read them back in UTC so the
  // displayed day doesn't shift with the build machine's timezone.
  config.addFilter("shortDate", (value) => new Date(value).toLocaleDateString("en-CA", {
    month: "short", day: "numeric", timeZone: "UTC",
  }));

  config.addFilter("longDate", (value) => new Date(value).toLocaleDateString("en-CA", {
    month: "long", day: "numeric", year: "numeric", timeZone: "UTC",
  }));

  // --- static assets --------------------------------------------------------
  // These were CopyPlugin patterns in vue.config.js. The image directories live
  // next to the content that references them, and are served from a flat path at
  // the site root, which is the path already baked into the data files and into
  // the blog HTML the Python converter emits.
  config.addPassthroughCopy({ CNAME: "CNAME" });
  // favicon.ico, robots.txt, sitemap.xml
  config.addPassthroughCopy({ public: "." });
  config.addPassthroughCopy({ "src/assets/images": "images" });
  config.addPassthroughCopy({ "src/assets/fonts": "fonts" });
  config.addPassthroughCopy({ "src/assets/resumes": "resumes" });
  config.addPassthroughCopy({ "src/assets/publications": "publications" });
  config.addPassthroughCopy({ "src/running/running-images": "running-images" });
  config.addPassthroughCopy({ "src/hiking/hiking-images": "hiking-images" });
  config.addPassthroughCopy({ "src/blog/content/images": "blog-images" });
  config.addPassthroughCopy({
    "src/bookshelf/syncer_v2/book_thumbnails_v2": "book_thumbnails_v2",
  });

  // --- Sass -----------------------------------------------------------------
  // Compiled through Eleventy rather than a separate `sass` CLI process so that
  // one command covers build, --serve and watch. Only src/styles/main.scss is
  // compiled; every other .scss file is a partial it @uses.
  config.addTemplateFormats("scss");
  config.addExtension("scss", {
    outputFileExtension: "css",
    compile(contents, inputPath) {
      const { css } = sass.compileString(contents, {
        loadPaths: [path.dirname(inputPath), "node_modules"],
        style: "compressed",
        sourceMap: false,
      });
      return () => css;
    },
  });
  config.ignores.add("src/styles/_*.scss");
  config.addWatchTarget("src/styles/");

  // --- what Eleventy must not treat as a template ---------------------------
  // The blog pipeline's markdown sources and the HTML Pandoc emits from them are
  // inputs to the data layer, not pages. The Python syncers own these paths.
  config.ignores.add("src/blog/content/");
  // Reference-only Vue components, kept until the sections that replace them
  // land (#535 onwards). Not a template format, but ignoring them keeps the
  // watcher quiet.
  config.ignores.add("src/**/*.vue");

  return {
    dir: {
      input: "src",
      output: "dist",
      includes: "_includes",
      data: "_data",
    },
    templateFormats: ["njk", "html", "11ty.js"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: false,
  };
};
