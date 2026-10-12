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
 *
 * A series post also carries `seriesPrevious` and `seriesNext`: the listed parts
 * either side of it in part order, for the series nav on the post page (#555).
 * Either is undefined at the end of a series.
 *
 * Each post also carries `image`: the first blog image in its body, used as the
 * index card's thumbnail. Seven of the 14 listed posts have no image at all, so
 * templates must handle it being null.
 *
 * `_show` and `_archived` are separate on purpose: 29 of the 43 shown posts are
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

// The card thumbnail on the blog index is the post's own first image, so
// nothing has to be authored or maintained alongside the post. Only
// /blog-images/ paths qualify: an absolute URL here would be a shields.io badge
// or similar rather than a picture of anything, and a local path is guaranteed
// to be a file the passthrough copy ships.
function firstImage(body) {
  const match = body.match(/<img\b[^>]*\bsrc="(\/blog-images\/[^"]+)"/);
  return match ? match[1] : null;
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
      image: firstImage(body),
      emoji: emojiFor(m._id, series),
      url: `/blog/${m._id}/`,
    };
  })
  .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

const listed = all.filter((p) => !p.archived);

// The previous and next parts of each series post. Ordered by part, not date:
// parts aren't always published in order. Built from `listed`, so an archived or
// unpublished part is skipped rather than linked to.
//
// The series name is only ever typed into a title, so a typo would quietly
// start a new one-part series with no nav. Every series has an icon, which
// makes SERIES_EMOJI the list of known names; fail the build on anything else,
// and on two posts claiming the same part (#555).
const seriesParts = new Map();
for (const post of listed) {
  if (!post.series) continue;
  const { name, part } = post.series;
  if (!SERIES_EMOJI[name]) {
    throw new Error(`blog.js: "${post.id}" is in unknown series "${name}". Fix the title prefix or add the series to SERIES_EMOJI.`);
  }
  if (!seriesParts.has(name)) seriesParts.set(name, []);
  const clash = seriesParts.get(name).find((p) => p.series.part === part);
  if (clash) {
    throw new Error(`blog.js: "${post.id}" and "${clash.id}" are both part ${part} of "${name}".`);
  }
  seriesParts.get(name).push(post);
}

const seriesLink = (p) => p && { part: p.series.part, displayTitle: p.displayTitle, url: p.url };

for (const parts of seriesParts.values()) {
  parts.sort((a, b) => a.series.part - b.series.part);
  parts.forEach((post, i) => {
    post.seriesPrevious = seriesLink(parts[i - 1]);
    post.seriesNext = seriesLink(parts[i + 1]);
  });
}

module.exports = { all, listed };
