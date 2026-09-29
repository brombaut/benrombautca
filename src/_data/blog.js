/*
 * Blog posts, merged and derived once at build time.
 *
 * Replaces BlogPostsProxy.ts. The two source JSON files stay where the Python
 * syncer pipeline writes them (src/blog/), so nothing about that pipeline
 * changes; this only reads them.
 *
 * Exposes:
 *   blog.all     every post with `_show`, newest first. These get a page.
 *   blog.listed  the subset that is also not `_archived`, newest first. These
 *                appear on the blog index.
 *   blog.byYear  `listed`, grouped by year, newest year first.
 *
 * `_show` and `_archived` are separate on purpose: 29 of the 42 shown posts are
 * archived, and the old hash router still resolved a URL for every one of them
 * even though the index hid them. Keeping a page for each preserves those links,
 * which #518 depends on.
 */
const meta = require("../blog/blog_posts_meta.json");
const content = require("../blog/blog_posts_content.json");

// A "[Series N] " title prefix marks a post as part of a series.
const SERIES_PREFIX = /^\[(.+?)\s+(\d+)\]\s*/;
const WORDS_PER_MINUTE = 225;

// Every post in a series shares its series icon.
const SERIES_EMOJI = {
  "AI Experience": "🧭",
  "AI Slop": "🧹",
  "SWE-bench Architecture": "🏗️",
  "Learning LLMs": "🧠",
};

// One-off posts that aren't part of a series can opt into their own icon.
const POST_EMOJI = {
  "20260710_aiware_observability": "🔭",
  "coding-agent-architectures": "🤖",
};

const DEFAULT_EMOJI = "📝";

function parseSeries(title) {
  const match = title.match(SERIES_PREFIX);
  if (!match) return null;
  return { name: match[1], part: Number(match[2]) };
}

function emojiFor(id, series) {
  if (series && SERIES_EMOJI[series.name]) return SERIES_EMOJI[series.name];
  return POST_EMOJI[id] || DEFAULT_EMOJI;
}

// The Pandoc pipeline writes image and PDF links relative to the page
// ("blog-images/foo.png"), which worked under hash routing because every page
// was served from the site root. Real nested URLs like /blog/<id>/ break them,
// so anchor them to the root here rather than changing the Python converter.
function rootRelative(body) {
  return body.replace(
    /(\s(?:src|href)=")(?!https?:|\/|#|mailto:|data:|")/g,
    "$1/",
  );
}

// Most posts open with an <h1> carrying the document title, which the page
// already renders above the body. The old site showed both. Drop the leading
// one; any later <h1> is a real section heading and stays.
function stripLeadingHeading(body) {
  return body.replace(/^\s*<h1[^>]*>[\s\S]*?<\/h1>/, "");
}

function readingMinutes(body) {
  const words = body.replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / WORDS_PER_MINUTE));
}

const bodies = new Map(content.map((c) => [c._id, c._body]));

const all = meta
  .filter((m) => m._show)
  .map((m) => {
    const body = stripLeadingHeading(rootRelative(bodies.get(m._id) || ""));
    const series = parseSeries(m._title);
    return {
      id: m._id,
      title: m._title,
      // The meta JSON stores UTC midnight timestamps; read them back in UTC so
      // the displayed day never shifts with the build machine's timezone.
      createdAt: m._createdAt,
      year: new Date(m._createdAt).getUTCFullYear(),
      description: m._description,
      archived: m._archived,
      body,
      series,
      // The title with any series prefix removed.
      displayTitle: m._title.replace(SERIES_PREFIX, ""),
      readingMinutes: readingMinutes(body),
      emoji: emojiFor(m._id, series),
      url: `/blog/${m._id}/`,
    };
  })
  .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

const listed = all.filter((p) => !p.archived);

const byYear = [...new Set(listed.map((p) => p.year))]
  .sort((a, b) => b - a)
  .map((year) => ({ year, posts: listed.filter((p) => p.year === year) }));

module.exports = { all, listed, byYear };
