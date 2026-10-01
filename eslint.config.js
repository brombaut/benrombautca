"use strict";

/*
 * Plain-JS lint config. `npm run lint` is a required step in both
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
      // Playwright type-checks its own TS config and spec files.
      "**/*.ts",
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
