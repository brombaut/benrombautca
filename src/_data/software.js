/*
 * Software projects, merged and derived once at build time.
 *
 * Replaces SoftwareArticlesProxy.ts. The two source JSON files stay where the
 * GitHub Action syncer writes them (src/software/).
 *
 * `_updatedAt` is not carried through: for three of the four projects it is the
 * syncer's own run time, all within a second of each other in June 2022, so it
 * says nothing about the project.
 */
const meta = require("../software/software_articles_meta.json");
const content = require("../software/software_articles_content.json");

const bodies = new Map(content.map((c) => [c._id, c._body]));

// Same as in blog.js. Every README opens with an <h1> of the project name and
// the page already renders the title above the body, so the old site showed it
// twice. Duplicated rather than shared: it is three lines and a _data/ module
// would become a data file named `_html`.
function stripLeadingHeading(body) {
  return body.replace(/^\s*<h1[^>]*>[\s\S]*?<\/h1>/, "");
}

// The syncer prefixes its field names with `_`; strip it so templates read
// normally. The entries already carry everything a template needs
// (imagePath, title, url), which is what makes ExternalRepoIcon.vue and
// TechUsedIcon.vue redundant.
function plain(entry) {
  return Object.fromEntries(
    Object.entries(entry).map(([k, v]) => [k.replace(/^_/, ""), v]),
  );
}

const projects = meta
  .filter((m) => m._show)
  .sort((a, b) => a._order - b._order)
  .map((m) => ({
    id: m._id,
    title: m._title,
    createdAt: m._createdAt,
    year: new Date(m._createdAt).getUTCFullYear(),
    description: m._description,
    body: stripLeadingHeading(bodies.get(m._id) || ""),
    externalRepos: (m._externalRepos || []).map(plain),
    techUsed: (m._techUsed || []).map(plain),
    url: `/software/${m._id}/`,
  }));

module.exports = { projects };
