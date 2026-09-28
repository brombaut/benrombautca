/*
 * Feature flags, read from the environment at build time.
 *
 * FLAG_MARATHON is the only environment variable the site actually consumes: it
 * gates the Running section. The seven VUE_APP_* Firebase secrets that CI used
 * to write into .env were never read anywhere and have been removed, along with
 * app_config.ts, which existed to validate them.
 *
 * The name dropped its VUE_APP_ prefix along with Vue; the GitHub Actions
 * workflows write the new name.
 */
module.exports = {
  marathon: process.env.FLAG_MARATHON === "true",
};
