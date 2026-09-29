/*
 * Running and Hiking: the entries, plus the two facts that used to be hardcoded
 * in the old templates (HikingSection.vue's `completedPeaks`, and the upcoming
 * race that was a literal <li> in RunningSection.vue).
 *
 * Sorting and filtering live here rather than in the templates, matching blog.js
 * and books.js.
 */
const hikes = require("./hikes.json");
const races = require("./races.json");

const newestFirst = (a, b) => b.orderDate.localeCompare(a.orderDate);

// Adirondack High Peaks completed, of the 46 over 4,000 feet.
const peaks = { completed: 22, total: 46 };

// Races entered but not yet run. A race drops off on its own once its date has
// passed, so a stale entry can't linger between edits.
const upcoming = [
  {
    name: "Quebec City Half Marathon",
    event: "Beneva Quebec City Marathon",
    date: "2026-10-05",
    url: "https://www.jecoursqc.com/en/beneva-quebec-city-marathon-presented-by-montellier/races/#/21-1k-shop-sante-presented-by-wknd-91-9",
  },
];

const today = new Date().toISOString().slice(0, 10);

module.exports = {
  // `visible: false` hides a hike; most entries omit the field entirely.
  hikes: hikes.filter((h) => h.visible !== false).sort(newestFirst),
  races: [...races].sort(newestFirst),
  peaks,
  peaksPercent: Math.round((peaks.completed / peaks.total) * 100),
  upcomingRaces: upcoming.filter((r) => r.date >= today),
};
