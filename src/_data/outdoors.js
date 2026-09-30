/*
 * Running and Hiking: the entries, plus the Adirondack peak count that used to
 * be hardcoded in HikingSection.vue.
 *
 * Sorting and filtering live here rather than in the templates, matching blog.js
 * and books.js.
 */
const hikes = require("./hikes.json");
const races = require("./races.json");

const newestFirst = (a, b) => b.orderDate.localeCompare(a.orderDate);

// Adirondack High Peaks completed, of the 46 over 4,000 feet.
const peaks = { completed: 22, total: 46 };

module.exports = {
  // `visible: false` hides a hike; most entries omit the field entirely.
  hikes: hikes.filter((h) => h.visible !== false).sort(newestFirst),
  races: [...races].sort(newestFirst),
  peaks,
};
