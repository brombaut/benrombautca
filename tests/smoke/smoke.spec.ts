/* eslint-disable no-restricted-syntax -- sequential for...of loops are clearer for browser steps */
import { test as base, expect } from "@playwright/test";

/*
 * The route matrix and the nav-click walk that used to live here were written
 * against the Vue app's hash routes (`/#/blog/<id>`) and its `#site-header` /
 * `section#<id>` markup. None of that exists in the static rewrite, and the
 * pages it would visit are not built yet, so this file is currently down to the
 * one page #534 produces.
 *
 * #544 restores the full coverage against real nested paths, adds the screenshot
 * baselines, and is a precondition for merging the rewrite to `main`. The error
 * fixture below is unchanged and is what #544 builds back on top of.
 */

// Console errors that are known and harmless. Add a substring here, with a
// comment explaining why, rather than loosening the check.
const ALLOWED_CONSOLE_ERRORS: string[] = [];

// Fails any test that logs a console error, throws an uncaught exception, or
// gets a failed response for a same-origin asset (CSS, image, PDF, ...).
const test = base.extend<{ pageProblems: string[] }>({
  pageProblems: [async ({ page, baseURL }, use) => {
    const problems: string[] = [];
    const { origin } = new URL(baseURL as string);
    const isThirdParty = (url: string) => !!url && !url.startsWith(origin);

    // Keep the tests hermetic: third-party scripts (e.g. the ClustrMaps visitor
    // counter) shouldn't be hit by CI or be able to fail the run.
    await page.route((url) => isThirdParty(url.href), (route) => route.abort());

    page.on("console", (msg) => {
      if (msg.type() !== "error") return;
      const text = msg.text();
      if (text.startsWith("Failed to load resource") && isThirdParty(msg.location().url)) return;
      if (ALLOWED_CONSOLE_ERRORS.some((allowed) => text.includes(allowed))) return;
      problems.push(`console.error: ${text} (${msg.location().url})`);
    });
    page.on("pageerror", (err) => {
      problems.push(`uncaught exception: ${err.message}`);
    });
    page.on("response", (res) => {
      if (res.url().startsWith(origin) && res.status() >= 400) {
        problems.push(`HTTP ${res.status()}: ${res.url()}`);
      }
    });
    page.on("requestfailed", (req) => {
      if (req.url().startsWith(origin)) {
        problems.push(`request failed: ${req.url()} (${req.failure()?.errorText})`);
      }
    });

    await use(problems);

    expect(problems, "page reported errors").toEqual([]);
  }, { auto: true }],
});

test("the home page renders with its stylesheet", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("main h1")).toBeVisible();
  await expect(page).toHaveTitle(/Ben Rombaut/);
  await expect(page.locator(".sidebar .sidenav a")).toHaveCount(7);
  const stylesheet = await page.request.get("/styles/main.css");
  expect(stylesheet.ok(), "main.css is served").toBe(true);
  await page.waitForLoadState("networkidle");
});

// Passthrough copy is easy to break silently, and every section that follows
// depends on these paths. One representative file from each copied tree.
const copiedAssets = [
  "/CNAME",
  "/favicon.ico",
  "/robots.txt",
  "/images/benrombaut.webp",
  "/resumes/BenRombaut_Resume.pdf",
  "/publications/Rombaut_Benjamin_J_202205_MSc.pdf",
  "/hiking-images/19_01_katahdin/19_katahdin1.webp",
  "/running-images/22fredericton_06.webp",
  "/blog-images/learning-llms-2/gqa-kv-cache-explained.svg",
  "/book_thumbnails_v2/10284614-the-clean-coder.webp",
];

test("static assets are copied to their expected paths", async ({ page }) => {
  for (const path of copiedAssets) {
    const res = await page.request.get(path);
    expect(res.ok(), `${path} is served`).toBe(true);
  }
});
