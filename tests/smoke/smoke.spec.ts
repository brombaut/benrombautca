/* eslint-disable no-restricted-syntax -- sequential for...of loops are clearer for browser steps */
import { test as base, expect } from "@playwright/test";

/*
 * Covers the pages the rewrite has built so far: the home page (#535) and the
 * blog (#537). The remaining sections get added as they land, and #544 does the
 * full sweep plus screenshot baselines before the cutover merge.
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
  await expect(page.locator(".sidebar .sidenav a")).toHaveCount(6);
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

test("the blog index lists posts by year", async ({ page }) => {
  await page.goto("/blog/");
  await expect(page.locator("h1")).toHaveText("Blog");
  expect(await page.locator(".year-heading").count()).toBeGreaterThan(0);
  expect(await page.locator(".dated-list__title").count()).toBeGreaterThan(0);
});

// One post with the lot: code blocks, tables and images. The old build sized
// every <pre> in JavaScript to stop it blowing out the layout; this asserts the
// CSS replacement holds, since nothing would throw if it didn't.

test("a post renders its body without overflowing the page", async ({ page }) => {
  await page.goto("/blog/20220626_titanic_dataset/");
  await expect(page.locator(".article-body")).toBeVisible();
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - window.innerWidth,
  );
  expect(overflow, "no horizontal page scroll").toBeLessThanOrEqual(0);
  await page.waitForLoadState("networkidle");
});

test("the publications page lists both groups and serves its PDFs", async ({ page }) => {
  await page.goto("/publications/");
  expect(await page.locator(".pub-list > li").count()).toBe(13);
  await expect(page.locator(".pub-authors__me").first()).toBeVisible();
  const pdf = await page.locator(".pub-links a[href^='/publications/']").first().getAttribute("href");
  expect((await page.request.get(pdf as string)).ok(), `${pdf} is served`).toBe(true);
});
