/*
 * Software projects, merged and derived once at build time.
 *
 * Replaces SoftwareArticlesProxy.ts. The two source JSON files stay where the
 * GitHub Action syncer writes them (src/software/).
 */
const meta = require("../software/software_articles_meta.json");
const content = require("../software/software_articles_content.json");

const bodies = new Map(content.map((c) => [c._id, c._body]));

// The `_`-prefixed field names come from the syncer's serialisation format;
// strip the prefix so templates read normally.
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
    updatedAt: m._updatedAt,
    description: m._description,
    body: bodies.get(m._id) || "",
    order: m._order,
    externalRepos: (m._externalRepos || []).map(plain),
    techUsed: (m._techUsed || []).map(plain),
    url: `/software/${m._id}/`,
  }));

module.exports = { projects };
