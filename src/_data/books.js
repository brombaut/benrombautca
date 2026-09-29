/*
 * Bookshelf, grouped once at build time.
 *
 * The source JSON stays where the Goodreads syncer writes it
 * (src/bookshelf/syncer_v2/all_books_flattened.json). The shelf split and the
 * by-year grouping are lifted out of BookshelfSection.vue; #538 builds the
 * templates on top of this.
 */
const all = require("../bookshelf/syncer_v2/all_books_flattened.json");

// Books are dated YYYY-MM-DD, so the year is the first four characters. Parsing
// them as Dates would read them as UTC midnight and then need UTC getters back
// out, which is how the old component got this subtly right by accident.
const yearOf = (date) => (date ? Number(date.slice(0, 4)) : 0);

const byShelf = (shelf) => all.filter((b) => b.shelf === shelf);

// Ratings are 2-5 and every read book has one, so filled stars alone are
// enough; no empty-star track needed.
const withStars = (b) => ({ ...b, stars: "\u2605".repeat(Number(b.rating) || 0) });

const read = byShelf("read")
  .sort((a, b) => (b.date_finished || "").localeCompare(a.date_finished || ""))
  .map(withStars);

const readByYear = [...new Set(read.map((b) => yearOf(b.date_finished)))]
  .sort((a, b) => b - a)
  .map((year) => ({ year, books: read.filter((b) => yearOf(b.date_finished) === year) }));

// Oldest first: the book that's been on the go longest leads, which is what
// the old component did.
const currentlyReading = byShelf("currently-reading")
  .sort((a, b) => (a.date_added || "").localeCompare(b.date_added || ""));

const toRead = byShelf("to-read").sort((a, b) => a.position - b.position);

module.exports = {
  all, read, readByYear, currentlyReading, toRead,
};
