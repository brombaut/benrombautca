/* eslint-disable no-restricted-syntax -- sequential for...of loops are clearer for browser steps */
import { test as base, expect } from "@playwright/test";

/*
 * Smoke coverage for the static site (#544): every section page and every blog
 * post URL, the sidebar nav above the 782px breakpoint and the <details> top bar
 * below it, the passthrough-copied assets, and the #518 redirects/sitemap/404.
 */

// The sidebar/top bar nav, and the full set of section pages. Mirrors
// src/_data/nav.js; there is no software section in the rewrite.
const sections: [string, string][] = [
  ["About", "/"],
  ["Blog", "/blog/"],
  ["Publications", "/publications/"],
  ["Bookshelf", "/bookshelf/"],
  ["Running", "/running/"],
  ["Hiking", "/hiking/"],
];

// Representative posts: one with tables and many code blocks, one with diagrams.
const samplePosts = [
  "/blog/20220626_titanic_dataset/",
  "/blog/20260904_learning_llms_2_architecture_variations/",
];

const MOBILE = { width: 390, height: 844 };

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

const horizontalOverflow = (page: import("@playwright/test").Page) =>
  page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);

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
  "/fonts/albert-sans-latin.woff2",
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

test("every section page renders with a heading, a title and its nav marked", async ({ page }) => {
  for (const [label, url] of sections) {
    await page.goto(url);
    await expect(page.locator("main h1")).toBeVisible();
    await expect(page).toHaveTitle(/Ben Rombaut/);
    await expect(page.locator(`.sidebar .sidenav a[aria-current="page"]`)).toHaveText(label);
    expect(await horizontalOverflow(page), `no horizontal page scroll on ${url}`).toBeLessThanOrEqual(0);
    await page.waitForLoadState("networkidle");
  }
});

test("the sidebar nav reaches every section", async ({ page }) => {
  await page.goto("/");
  for (const [label, url] of sections) {
    await page.locator(".sidebar .sidenav a", { hasText: label }).click();
    await expect(page).toHaveURL(new RegExp(`${url.replace(/\//g, "\\/")}$`));
    await expect(page.locator("main h1")).toBeVisible();
  }
});

test("the top bar nav takes over below the breakpoint", async ({ page }) => {
  await page.setViewportSize(MOBILE);
  await page.goto("/");
  await expect(page.locator(".sidebar")).toBeHidden();
  await expect(page.locator(".topbar")).toBeVisible();

  // The menu is a <details>, so it opens with no JavaScript.
  const menu = page.locator(".topnav");
  await expect(menu.locator(".topnav__list")).toBeHidden();
  await menu.locator("summary").click();
  await expect(menu.locator("a")).toHaveCount(sections.length + 3); // + social links

  await menu.locator("a", { hasText: "Bookshelf" }).click();
  await expect(page).toHaveURL(/\/bookshelf\/$/);
  await expect(page.locator("main h1")).toHaveText("Bookshelf");
});

test("pages fit the mobile viewport", async ({ page }) => {
  await page.setViewportSize(MOBILE);
  for (const url of [...sections.map(([, u]) => u), ...samplePosts]) {
    await page.goto(url);
    await expect(page.locator("main h1")).toBeVisible();
    expect(await horizontalOverflow(page), `no horizontal page scroll on ${url}`).toBeLessThanOrEqual(0);
    await page.waitForLoadState("networkidle");
  }
});

test("the blog index lists posts by year and links to pages that exist", async ({ page }) => {
  await page.goto("/blog/");
  await expect(page.locator("h1")).toHaveText("Blog");
  expect(await page.locator(".year-heading").count()).toBeGreaterThan(0);

  // Only the `listed` posts appear here; the unlisted ones still get a page.
  const links = await page.locator("a.dated-list__title").evaluateAll(
    (els) => els.map((el) => (el as HTMLAnchorElement).getAttribute("href") as string),
  );
  expect(links.length, "posts are listed").toBeGreaterThan(10);
  for (const href of links) {
    expect((await page.request.get(href)).ok(), `${href} is built`).toBe(true);
  }
});

// A post page that fails to build is invisible from the index (most posts are
// unlisted), so walk every post URL the sitemap advertises instead.
test("every blog post URL in the sitemap is built", async ({ page }) => {
  const xml = await (await page.request.get("/sitemap.xml")).text();
  const posts = [...xml.matchAll(/<loc>[^<]*(\/blog\/[^<]+\/)<\/loc>/g)].map((m) => m[1]);
  expect(posts.length, "posts are in the sitemap").toBe(42);
  for (const url of posts) {
    const res = await page.request.get(url);
    expect(res.ok(), `${url} is built`).toBe(true);
    expect(await res.text(), `${url} has a body`).toContain("article-body");
  }
});

// One post with the lot: code blocks, tables and images. The old build sized
// every <pre> in JavaScript to stop it blowing out the layout; this asserts the
// CSS replacement holds, since nothing would throw if it didn't.

test("a post renders its body without overflowing the page", async ({ page }) => {
  await page.goto("/blog/20220626_titanic_dataset/");
  await expect(page.locator(".article-body")).toBeVisible();
  expect(await horizontalOverflow(page), "no horizontal page scroll").toBeLessThanOrEqual(0);
  await page.waitForLoadState("networkidle");
});

test("the publications page lists both groups and serves its PDFs", async ({ page }) => {
  await page.goto("/publications/");
  expect(await page.locator(".pub-list > li").count()).toBe(13);
  await expect(page.locator(".pub-authors__me").first()).toBeVisible();
  const pdf = await page.locator(".pub-links a[href^='/publications/']").first().getAttribute("href");
  expect((await page.request.get(pdf as string)).ok(), `${pdf} is served`).toBe(true);
});

test("the bookshelf renders books grouped by year", async ({ page }) => {
  await page.goto("/bookshelf/");
  await expect(page.locator("h1")).toHaveText("Bookshelf");
  expect(await page.locator(".book").count()).toBeGreaterThan(100);
  await expect(page.locator(".book__cover").first()).toBeVisible();
  await page.waitForLoadState("networkidle");
});

test("hiking and running render their entries and scroll galleries internally", async ({ page }) => {
  await page.goto("/hiking/");
  expect(await page.locator(".entry").count()).toBe(37);
  await expect(page.locator(".progress__fill")).toHaveAttribute("style", /width: \d+%/);

  await page.goto("/running/");
  expect(await page.locator(".entry").count()).toBe(5);
  // The image strip must scroll inside itself, not widen the page.
  const gallery = page.locator(".gallery").first();
  const scrolls = await gallery.evaluate((el) => el.scrollWidth > el.clientWidth);
  expect(scrolls, "gallery scrolls horizontally").toBe(true);
  expect(await horizontalOverflow(page), "no horizontal page scroll").toBeLessThanOrEqual(0);
  await page.waitForLoadState("networkidle");
});

// #518. Old hash URLs all request "/", so an inline script in the home page's
// <head> does the mapping. These are the URLs that exist in the wild.
const hashRedirects: [string, string][] = [
  ["/#/about-me", "/"],
  ["/#/work", "/"],
  ["/#/education", "/"],
  ["/#/blog", "/blog/"],
  ["/#/blog/20210624_deploy_ghpages_actions", "/blog/20210624_deploy_ghpages_actions/"],
  ["/#/articles", "/blog/"],
  ["/#/articles/prime_numbers", "/blog/"],
  ["/#/software", "/"],
  ["/#/software/game_of_life", "/"],
  ["/#/publications", "/publications/"],
  ["/#/bookshelf", "/bookshelf/"],
  ["/#/running", "/running/"],
  ["/#/hiking", "/hiking/"],
];

test("old hash URLs redirect to their real paths", async ({ page, baseURL }) => {
  for (const [from, to] of hashRedirects) {
    await page.goto(from);
    await page.waitForURL(new URL(to, baseURL).href);
    await expect(page.locator("main h1")).toBeVisible();
  }
});

test("the sitemap is generated from the page list", async ({ page }) => {
  const res = await page.request.get("/sitemap.xml");
  expect(res.ok(), "sitemap.xml is served").toBe(true);
  const xml = await res.text();
  expect(xml, "no stale hash URLs").not.toContain("/#/");
  expect(xml).toContain("<loc>https://www.benrombaut.ca/blog/20210624_deploy_ghpages_actions/</loc>");
  // Every built page, and nothing else: 6 sections plus one page per post.
  expect(xml.match(/<url>/g)?.length).toBe(48);
});

test("404.html is a real page with a way back", async ({ page }) => {
  await page.goto("/404.html");
  await expect(page.locator("main h1")).toHaveText("Page not found");
  await expect(page.locator(".buttons a[href='/']")).toBeVisible();
});
