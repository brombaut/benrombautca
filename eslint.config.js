"use strict";

/*
 * Plain-JS lint config, replacing the Vue + Airbnb + TypeScript stack that went
 * away with Vue CLI. `npm run lint` is a required step in both
 * install_lint_build.yml and gh_pages_deploy.yml, so this has to keep passing.
 *
 * The rules are deliberately thin: correctness checks plus the two formatting
 * conventions the codebase actually holds to (double quotes, 2-space indent).
 */
const js = require("@eslint/js");

module.exports = [
  {
    ignores: [
      "dist/",
      "node_modules/",
      "venvs/",
      "test-results/",
      "playwright-report/",
      // Reference-only Vue components, deleted as the sections that replace them
      // land (#535 onwards). Nothing builds them and this config cannot parse
      // them.
      "src/**/*.vue",
      // Playwright type-checks its own TS config and spec files.
      "**/*.ts",
      // Written by the software syncer, not by hand.
      "**/f3_syncer.js",
    ],
  },
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: "commonjs",
      globals: {
        require: "readonly",
        module: "writable",
        process: "readonly",
        console: "readonly",
        __dirname: "readonly",
        URL: "readonly",
        Buffer: "readonly",
      },
    },
    rules: {
      quotes: ["error", "double"],
      indent: ["error", 2],
      semi: ["error", "always"],
      "comma-dangle": ["error", "always-multiline"],
      "no-console": "off",
    },
  },
];
