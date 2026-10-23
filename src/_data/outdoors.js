/*
 * Running and Hiking: the entries, plus the Adirondack peak count that used to
 * be hardcoded in HikingSection.vue.
 *
 * Sorting and filtering live here rather than in the templates, matching blog.js
 * and books.js.
 */
const fs = require("fs");
const path = require("path");
const hikes = require("./hikes.json");
const races = require("./races.json");

const newestFirst = (a, b) => b.orderDate.localeCompare(a.orderDate);

// The gallery shows photos at a fixed height and their own width, so each <img>
// needs width and height attributes, or a lazy image has no width until it loads
// and the strip jumps. Every gallery photo is WebP (convert_images_to_webp.py),
// and its size sits in the header, so it is read here instead of being stored.
// "hiking-images/..." lives in src/hiking/hiking-images/..., likewise running.
function webpSize(src) {
  const file = path.join(__dirname, "..", src.split("-")[0], src);
  const b = fs.readFileSync(file);
  const chunk = b.toString("ascii", 12, 16);
  if (chunk === "VP8 ") return { width: b.readUInt16LE(26) & 0x3fff, height: b.readUInt16LE(28) & 0x3fff };
  if (chunk === "VP8L") {
    const bits = b.readUInt32LE(21);
    return { width: (bits & 0x3fff) + 1, height: ((bits >> 14) & 0x3fff) + 1 };
  }
  if (chunk === "VP8X") return { width: b.readUIntLE(24, 3) + 1, height: b.readUIntLE(27, 3) + 1 };
  throw new Error(`${src}: not a WebP file`);
}

const withSizes = (entry) => ({
  ...entry,
  images: entry.images.map((img) => ({ ...img, ...webpSize(img.src) })),
});

// Adirondack High Peaks completed, of the 46 over 4,000 feet.
const peaks = { completed: 22, total: 46 };

module.exports = {
  // `visible: false` hides a hike; most entries omit the field entirely.
  hikes: hikes.filter((h) => h.visible !== false).map(withSizes).sort(newestFirst),
  races: races.map(withSizes).sort(newestFirst),
  peaks,
};
