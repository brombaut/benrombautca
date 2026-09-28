/* eslint-disable no-restricted-syntax -- sequential for...of loops are clearer for browser steps */
import { test as base, expect, Page } from "@playwright/test";
import blogPostsMeta from "../../src/blog/blog_posts_meta.json";
import softwareMeta from "../../src/software/software_articles_meta.json";

// Console errors that are known and harmless. Add a substring here, with a
// comment explaining why, rather than loosening the check.
const ALLOWED_CONSOLE_ERRORS: string[] = [];

// Fails any test that logs a console error, throws an uncaught exception, or
// gets a failed response for a same-origin asset (JS chunk, image, PDF, ...).
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

const firstBlogPost = blogPostsMeta.find((p) => p._show && !p._archived);
const firstSoftware = softwareMeta.find((s) => s._show);

interface RouteCase {
  path: string;
  // Ids of the <section> elements that must be visible with a title.
  sections: string[];
}

const routes: RouteCase[] = [
  { path: "/", sections: ["about-me", "work-education"] },
  { path: "/about-me", sections: ["about-me", "work-education"] },
  { path: "/work", sections: ["about-me", "work-education"] },
  { path: "/education", sections: ["about-me", "work-education"] },
  { path: "/bookshelf", sections: ["bookshelf"] },
  { path: "/blog", sections: ["blog"] },
  { path: `/blog/${firstBlogPost?._id}`, sections: ["selected-article"] },
  { path: "/software", sections: ["software"] },
  { path: `/software/${firstSoftware?._id}`, sections: ["selected-software"] },
  { path: "/publications", sections: ["publications"] },
  { path: "/running", sections: ["races"] },
  { path: "/hiking", sections: ["hikes"] },
];

async function expectSectionsVisible(page: Page, sections: string[]): Promise<void> {
  await expect(page.locator("#site-header")).toBeVisible();
  for (const id of sections) {
    const section = page.locator(`section#${id}`);
    await expect(section).toBeVisible();
    await expect(section.locator(".section-title").first()).toBeVisible();
    await expect(section.locator(".section-title").first()).not.toBeEmpty();
  }
}

test("test data has a visible blog post and software project", () => {
  expect(firstBlogPost, "no visible blog post in blog_posts_meta.json").toBeDefined();
  expect(firstSoftware, "no visible project in software_articles_meta.json").toBeDefined();
});

for (const route of routes) {
  test(`renders ${route.path}`, async ({ page }) => {
    await page.goto(`/#${route.path}`);
    await expectSectionsVisible(page, route.sections);
    // Let lazy-loaded images and late errors surface before the fixture checks.
    await page.waitForLoadState("networkidle");
  });
}

const navItems: { text: string; path: string; sections: string[] }[] = [
  { text: "Publications", path: "/publications", sections: ["publications"] },
  { text: "Bookshelf", path: "/bookshelf", sections: ["bookshelf"] },
  { text: "Blog", path: "/blog", sections: ["blog"] },
  { text: "Running", path: "/running", sections: ["races"] },
  { text: "Hiking", path: "/hiking", sections: ["hikes"] },
  { text: "About Me", path: "/about-me", sections: ["about-me", "work-education"] },
];

test("header nav links reach every section", async ({ page }) => {
  await page.goto("/#/");
  await expectSectionsVisible(page, ["about-me"]);

  const navLinks = page.locator(".full-navbar .full-nav-item");
  await expect(navLinks).toHaveCount(navItems.length);

  for (const item of navItems) {
    await navLinks.filter({ hasText: item.text }).click();
    await expect(page).toHaveURL(new RegExp(`#${item.path}$`));
    await expectSectionsVisible(page, item.sections);
  }
});
