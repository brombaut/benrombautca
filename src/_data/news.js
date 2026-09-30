/*
 * The home page News list: the latest few things added anywhere on the site,
 * pulled from each section's own data so nothing is maintained twice. Books are
 * deliberately left out (they would crowd out everything else), and so are
 * races not yet run. `milestones.json` holds one-off events, like job changes,
 * that no other data file records.
 */
const blog = require("./blog.js");
const outdoors = require("./outdoors.js");
const publications = require("./publications.json");
const milestones = require("./milestones.json");

const LIMIT = 5;

// Some hike and race dates are free text; only real dates can be ordered.
const isDate = (value) => /^\d{4}-\d{2}-\d{2}/.test(value || "");
const today = new Date().toISOString().slice(0, 10);

const items = [
  ...blog.listed.map((p) => ({
    date: p.createdAt.slice(0, 10),
    kind: "New blog post",
    title: `${p.emoji} ${p.displayTitle}`,
    url: p.url,
  })),
  ...publications.map((p) => ({
    date: p.dateAccepted,
    kind: "Paper accepted",
    title: p.title,
    url: "/publications/",
  })),
  ...outdoors.hikes.map((h) => ({ date: h.date, kind: "Hiked", title: h.name, url: "/hiking/" })),
  ...outdoors.races.map((r) => ({ date: r.date, kind: "Raced", title: r.name, url: "/running/" })),
  ...milestones.map((m) => ({ kind: "Career", ...m })),
];

module.exports = items
  .filter((i) => isDate(i.date) && i.date <= today)
  .sort((a, b) => b.date.localeCompare(a.date))
  .slice(0, LIMIT);
