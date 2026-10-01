# Agent Instructions

Guidance for AI coding agents working in this repository.

`CLAUDE.md` is a symlink to this file, so Claude Code and any tool that reads
`AGENTS.md` see exactly the same instructions. Edit this file, never the symlink.

## Status: static rewrite in progress

This branch (`redesign/static-rewrite`) is rewriting the site from a Vue 3 SPA
into a framework-free static site built with Eleventy. See issue #501 for the
plan and the go/no-go checkpoint, and #534 for the build scaffold that landed
first.

Every sub-issue of #501 has landed, the manual pass over all ~55 pages is done,
and the reference-only Vue components are now deleted, so everything in this file
describes the Eleventy site. All that remains is the cutover merge itself.

`main` still builds and deploys the Vue site, and does so until the single
cutover merge described in #501.

## Issue Tracking

This project uses **GitHub Issues** for issue tracking, driven from the terminal with the `gh` CLI — not beads, and no longer a local `issues.db` SQLite file. See `ISSUES.md` for the label conventions and the command reference.

Priority and type are labels (`p0`–`p4`, and `epic`/`feature`/`task`/`bug`). Epics are parents and their children are attached as GitHub sub-issues.

When reporting the status of any issue, always query GitHub directly (`gh issue view <number>`) rather than relying on conversation context — issue state may have changed elsewhere.

Because GitHub holds the issue state, there is nothing to `git pull` before reading issues and nothing to commit or push after changing them.

## Non-Interactive Shell Commands

**ALWAYS use non-interactive flags** with file operations to avoid hanging on confirmation prompts.

Shell commands like `cp`, `mv`, and `rm` may be aliased to include `-i` (interactive) mode on some systems, causing the agent to hang indefinitely waiting for y/n input.

**Use these forms instead:**
```bash
# Force overwrite without prompting
cp -f source dest           # NOT: cp source dest
mv -f source dest           # NOT: mv source dest
rm -f file                  # NOT: rm file

# For recursive operations
rm -rf directory            # NOT: rm -r directory
cp -rf source dest          # NOT: cp -r source dest
```

**Other commands that may prompt:**
- `scp` - use `-o BatchMode=yes` for non-interactive
- `ssh` - use `-o BatchMode=yes` to fail instead of prompting
- `apt-get` - use `-y` flag
- `brew` - use `HOMEBREW_NO_AUTO_UPDATE=1` env var

## Project Overview

**benrombautca** is Ben Rombaut's personal portfolio website, deployed at [benrombaut.ca](https://www.benrombaut.ca). This is a Vue 3 single-page application built with TypeScript, featuring a personal portfolio with multiple sections including About Me, Work/Education timeline, Publications, Blog, Software projects, Bookshelf, Running, and Hiking.

### Tech Stack
- **Generator**: Eleventy 3 (a build-time static site generator; no runtime framework ships)
- **Templating**: Nunjucks (`.njk`), with derived data computed in JS at build time
- **Language**: plain JavaScript (TypeScript was removed with the Vue toolchain)
- **Routing**: none. Real nested paths, one output file per page
- **Styling**: SCSS, compiled through Eleventy from a single `src/styles/main.scss`
- **Icons**: inline SVG (#536)
- **Deployment**: GitHub Pages
- **Automation**: GitHub Actions

## Repository Structure

```
benrombautca/
├── .github/workflows/          # GitHub Actions workflows
│   ├── gh_pages_deploy.yml    # Main deployment workflow
│   ├── sync_bookshelf.yml     # Bookshelf syncing automation
│   └── install_lint_build.yml # CI checks (lint, build, smoke tests)
├── public/                     # Static assets
├── scripts/                    # Utility scripts
│   ├── diagrams/              # Blog diagram generators (Python -> SVG + PNG)
│   ├── sync_bookshelf.sh      # Local bookshelf sync script
│   ├── sync_articles.sh       # Local articles sync script
│   └── *.py                   # Image processing utilities
├── src/                        # Eleventy input directory
│   ├── _data/                 # Global data: JSON content + derived JS data files
│   ├── _includes/             # Layouts and partials
│   ├── index.njk              # Home page
│   ├── bio.njk                # Bio page: career phases, newest first
│   ├── blog.njk               # Blog index
│   ├── blog-post.njk          # Blog post pages (paginated over every post)
│   ├── bookshelf.njk          # Bookshelf page
│   ├── publications.njk       # Publications page
│   ├── running.njk            # Running page
│   ├── hiking.njk             # Hiking page
│   ├── 404.njk                # Builds /404.html
│   ├── sitemap.njk            # Builds /sitemap.xml
│   ├── assets/                # Fonts, images, resumes, publications PDFs
│   ├── blog/                  # Blog JSON + the content pipeline
│   │   └── content/           # Blog post sources (MD) and converted (HTML)
│   ├── bookshelf/             # Bookshelf data
│   │   └── syncer_v2/         # Goodreads scraping and syncing logic
│   ├── hiking/hiking-images/  # Hiking photos
│   ├── running/running-images/ # Running photos
│   └── styles/                # SCSS
├── tests/smoke/               # Playwright smoke tests (every route renders, no console errors)
├── playwright.config.ts       # Playwright config (serves dist/)
├── AGENTS.md                  # This file: agent/AI guidance (canonical)
├── CLAUDE.md                  # Symlink -> AGENTS.md
├── package.json               # Dependencies and scripts
├── eleventy.config.js         # Eleventy config: passthrough copy, Sass, ignores
└── eslint.config.js           # Flat ESLint config for plain JS
```

## Key Architecture Patterns

### Templates and the data layer

There are no components. A page is a `.njk` template with front matter naming its
layout; shared markup goes in `src/_includes/` as a layout or a partial.

All content reaches templates through Eleventy's global data layer in
`src/_data/`, which is the *only* place derived values are computed. That
computation happens once per build, not per render:

| File | What it provides |
| --- | --- |
| `hikes.json`, `races.json`, `publications.json`, `aboutMe.json` | Hand-authored content, migrated out of the old `.ts` files |
| `blog.js` | Merges `blog_posts_meta.json` + `blog_posts_content.json`; series parsing, emoji, reading time, sorting, and the `all` / `listed` split |
| `books.js` | Splits `all_books_flattened.json` by shelf and groups read books by year |
| `outdoors.js` | Hikes and races, sorted newest first; the 46er count and the upcoming-race list |
| `news.js` | The home page News list: the 5 newest dated items across listed blog posts, publications, hikes, past races and `milestones.json`. Books are left out on purpose |
| `milestones.json` | Hand-authored one-off events for News that no other file records, e.g. job changes |
| `site.js` | Site title, description, canonical URL, ClustrMaps script src |

There is no `work.json` / `education.json`. #543 was dropped, so there is no
Work/Education section: the career history is hand-written prose in `src/bio.njk`,
and the two source-note files were deleted once nothing read them.

The JSON written by the Python and GitHub Actions syncers stays exactly where
those syncers put it (`src/blog/`, `src/bookshelf/syncer_v2/`)
and is read in place. **Never move those files.**

### Dates in the data files

The migrated JSON stores dates as date-only ISO strings (`"2019-07-21"`), never
as timestamps. The old `.ts` sources wrote `new Date(2019, 6, 21)`, which is
local time with a **zero-indexed month** (July, not June), and `.toISOString()`
on a local midnight shifts the calendar day for any timezone east of UTC.
Date-only strings sidestep both traps. `blog_posts_meta.json` is the exception:
the syncer writes UTC timestamps there, so read them back with `getUTC*`.

### Routing

None. Eleventy writes one HTML file per page and the paths are real:
`/blog/<postId>/`. The old Vue hash URLs (`/#/blog/<postId>`) are handled by a
small inline script in `src/_includes/hash-redirect.njk`, included in `<head>` on
the home page only, since every hash URL requests `/` (#518). It holds an
explicit mapping table and `location.replace`s to the new path. `/#/about-me`
goes to `/` (the About content is the home page) and `/#/work` and
`/#/education` go to `/bio/` (#545);
`/#/software` and `/#/software/<id>` go to `/` (that section is deleted);
`/#/articles` and `/#/articles/<slug>` go to `/blog/` (those slugs lack the date
prefix real post ids have, so they can't be mapped to a post).

`src/404.njk` builds `/404.html`, which GitHub Pages serves for unmatched paths.
It is a real 404 page, not the old SPA-routing hack.

`src/sitemap.njk` generates `/sitemap.xml` from `collections.all` at build time,
so it can't drift. The hand-maintained `public/sitemap.xml` is gone.
`blog-post.njk` sets `pagination.addAllPagesToCollections: true` so every post
reaches that collection. `public/robots.txt` points at
`https://www.benrombaut.ca/sitemap.xml`, which is still correct.

### Shared Markup
Shared markup lives in `src/_includes/` as layouts and partials:
- `base.njk` - The HTML shell: head, canonical link, og/twitter tags, stylesheet
  link, ClustrMaps script
- `hash-redirect.njk` - The old-hash-URL redirect script (#518), included on `/` only

#501 rules that not every old shared component needs an equivalent.
`SkeletonLoader.vue` is already gone (nothing loads on a static site), and the
carousel is expected to become CSS scroll-snap rather than JavaScript (#541).

### Styling System

#### Stylesheets
`src/styles/main.scss` is the single entry point and the only file Eleventy
compiles; everything else in `src/styles/` is a Sass partial with a leading
underscore that `main.scss` `@use`s. It compiles to `/styles/main.css`.

- `_github_article.scss` - GitHub-flavoured styling for rendered markdown bodies
  (blog posts). Standalone, references no tokens.

The design system (tokens, fluid type scale, the left-right layout shell) lands
in #535. The old `variables.scss` blue palette, `common.scss`, and
`keyframes.scss` were deleted rather than carried over: #501 replaces the palette
with an indigo scheme and rules out animation in this pass.

There is no auto-import of globals any more. A partial that needs tokens `@use`s
them explicitly.

#### Colour Scheme
Per #501, one scheme only, no dark variant:

| Token | Value |
| --- | --- |
| background | `#fff` |
| foreground | `#111` |
| primary | `#5857ff` |
| secondary | `#6b6a6a` |
| tertiary | `#e2e2e2` |
| quaternary | `#f3f2f2` |

#### Responsive Breakpoint
A single breakpoint at **782px**: above it the left sidebar shows, below it a top
bar with a hamburger. See #501 and #277.

## Content Management & Syncing

### Blog
- **Source**: Markdown files in `src/blog/content/sources_md/`
- **Conversion**: Python scripts convert MD → HTML using Pandoc
- **Scripts**:
  - `00_ipynb_to_md_converter.py` - Jupyter notebooks to markdown
  - `01_md_to_html_converter.py` - Markdown to HTML
  - `02_existing_html_articles_syncer.py` - Sync to content JSON
- **Output**: `src/blog/content/converted_html/`
- **Metadata**: Manually maintained in `blog_posts_meta.json`
- **IMPORTANT**: Never directly edit `blog_posts_content.json`. It is generated by the syncer pipeline. Always edit the source markdown file in `sources_md/`, then re-run `01_md_to_html_converter.py` and `02_existing_html_articles_syncer.py` to regenerate it.

### Blog Diagrams
- **Source**: Python generators in `scripts/diagrams/` (one `d_*.py` per diagram)
- **Output**: `.svg` and `.png` written to `src/blog/content/images/<post-slug>/`
- **Rebuild**: `python3 scripts/diagrams/build.py`, or a single `d_*.py`
- **IMPORTANT**: Never hand-edit a generated SVG. Edit the `d_*.py` and rebuild, the
  same rule that applies to `blog_posts_content.json`.
- Boxes are sized from real font metrics, so text cannot silently overflow. The build
  prints `!!` warnings when something does not fit.
- See `scripts/diagrams/README.md` for dependencies, the layout skeleton, and the palette.

### Bookshelf
- **Source**: Goodreads user profile (web scraping)
- **Pipeline**:
  1. `00_goodreads_scraper.py` - Scrapes Goodreads profile
  2. `02_all_books_flattener.py` - Flattens book data structure
  3. `03_show_missing_thumbnails.py` - Reports missing covers
  4. `04_download_missing_thumbnails.py` - Fetches the covers reported missing
- **Automation**: GitHub Actions (currently `workflow_dispatch` only, cron commented out)
- **Data**: `src/bookshelf/syncer_v2/all_books_flattened.json`

## Development Workflows

### Local Development

```bash
# Install dependencies
npm install

# Start dev server with live reload (http://localhost:8080)
npm run serve

# Build for production into dist/ (cleans dist/ first)
npm run build

# Lint and fix code issues
npm run lint

# Build and run the browser smoke tests
npm run test:smoke:build

# Sync bookshelf locally
npm run sync-bookshelf

# Sync blog locally
npm run sync-articles


# Regenerate blog diagrams
python3 scripts/diagrams/build.py
```

### Environment Variables
**None.** The build reads no environment variables at all, so CI writes no `.env`.

`FLAG_MARATHON` was the last one standing after #534, but #541 found it gated
nothing: `FullNavBar.vue` assigned it into `data()` and no template ever read it,
so the Running nav item was unconditional. It went, along with `src/_data/flags.js`,
the `.env` step in both workflows, and the `dotenv` dependency. The seven
`VUE_APP_*` Firebase secrets went the same way in #534, and all of those GitHub
Secrets have since been deleted. `BOOKSHELF_PAT` is the only repository secret
left, and no workflow references it: `sync_bookshelf.yml` pushes with the
built-in `GITHUB_TOKEN`.

### Git Workflow
- **Main Branch**: `main`
- **Deployment**: Automatic on push to `main` via GitHub Actions
- **Protected Branch**: Deploys to `gh-pages` branch

## Coding Conventions

### TypeScript/JavaScript
- **Indentation**: 2 spaces
- **Quotes**: Double quotes (`"`)
- **Semicolons**: Not enforced
- **ESLint**: `eslint.config.js`, flat config, `eslint:recommended` plus double
  quotes and 2-space indent. `npm run lint` is a required CI step and a failure
  blocks the deploy

### File Naming
- **Templates**: kebab-case (e.g. `about-me.njk`), matching their output path
- **Data files**: match the variable name templates use (`hikes.json` → `hikes`)

### Imports
Node `require` with relative paths. There is no `@/` alias any more. Data files
read the syncer-owned JSON in place:

```javascript
const meta = require("../blog/blog_posts_meta.json");
```

## Build & Deployment

### Build Process
```bash
npm run build
```
Runs `rm -rf dist` and then `eleventy`. Outputs to `dist/`:
- One HTML file per page, no JS bundle
- `styles/main.css`, compiled and minified from `src/styles/main.scss`
- `sitemap.xml`, generated from the page list, and `404.html`
- Copied static assets (CNAME, favicon, robots.txt, images, PDFs)

Sass is compiled *through* Eleventy (a custom extension in `eleventy.config.js`)
rather than by a separate `sass` CLI process, so one command covers build,
`--serve` and watch.

### GitHub Actions Deployment
**Workflow**: `.github/workflows/gh_pages_deploy.yml`

Triggers:
- Push to `main` branch
- Completion of `bookshelf-syncer` workflow

Steps:
1. Checkout code
2. Install and Build - runs `npm install`, then `npm run lint`, then `npm run build`
   (lint is enforced here; a violation fails the deploy)
3. Install Playwright Chromium
4. Smoke Test - runs `npm run test:smoke` against the build (a failure blocks the deploy)
5. Deploy to `gh-pages` branch

### Static Asset Copying
`eleventy.config.js` uses passthrough copy for:
- `CNAME` → root (for custom domain)
- Book thumbnails → `book_thumbnails_v2/`
- Resumes → `resumes/`
- Publications → `publications/`
- Running images → `running-images/`
- Hiking images → `hiking-images/`
- Blog images (`src/blog/content/images`) → `blog-images/`
- Component images (`src/assets/images`) → `images/` (replaces the old webpack
  `require.context` lookup in `ui-utils.ts`)
- `public/` → root (favicon.ico, robots.txt). `sitemap.xml` is generated, not copied

These flat root paths are already baked into the migrated data files and into the
HTML the blog converter emits, which is why they are kept as-is.

## Testing

**Status**: Browser smoke tests (Playwright) plus ESLint. No unit tests yet.

The smoke tests in `tests/smoke/` load the **production build** in headless Chromium,
against the real nested paths (#544). What runs:
- The home page renders and its stylesheet is served
- One representative file from every passthrough-copied tree is reachable
- Every section page renders its entries, has a title, and marks its nav item
- The sidebar nav reaches every section above 782px, and below it the `<details>`
  top bar menu opens and navigates with no JavaScript
- Nothing overflows horizontally at 390px, on every section page and two
  content-heavy posts
- Every blog post URL in the sitemap is built with a body (most posts are
  unlisted, so the index alone doesn't cover them)
- Every old hash URL redirects to its real path, `/sitemap.xml` has no hash URLs,
  and `/404.html` renders
- Any `console.error`, uncaught exception, or failed same-origin request
  (CSS, images, PDFs) fails the run

There are deliberately **no screenshot baselines**, and none are planned. A set was
committed under #544 and removed again in 748f4d5: they needed regenerating after
every design change, and because text rasterisation differs from CI's
`ubuntu-latest` they had to be skipped there anyway, which left a check that only
ran locally and mostly reported its own staleness. Not worth the upkeep. The
functional smoke tests above are the safety net.

Third-party requests (e.g. the ClustrMaps visitor counter) are blocked so the tests are
hermetic. A known-harmless console error can be added to `ALLOWED_CONSOLE_ERRORS` in
`tests/smoke/smoke.spec.ts`, with a comment explaining why; don't loosen the check instead.

```bash
npx playwright install chromium   # one-time browser download
npm run test:smoke:build          # build, then run the smoke tests
npm run test:smoke                # run against an existing dist/
```

`playwright.config.ts` serves `dist/` with `tests/smoke/serve-dist.js` (no extra
dependency). If a preinstalled Chromium doesn't match the Playwright version, point
`PLAYWRIGHT_CHROMIUM_EXECUTABLE` at it. Playwright transpiles its own `.ts` files,
which is why the config and spec stay TypeScript with no `typescript` dependency.

CI runs the smoke tests on every PR (`install_lint_build.yml`, which triggers on PRs
into `main` *and* into `redesign/static-rewrite`) and before deploying
(`gh_pages_deploy.yml`), so a broken view never ships.

## Common Development Tasks

### Adding a New Blog Post
1. Write post in Markdown: `src/blog/content/sources_md/post-name.md`
2. Run conversion script from `src/blog/content/`: `python 01_md_to_html_converter.py`
3. Run sync script from `src/blog/content/`: `python 02_existing_html_articles_syncer.py`
   - This adds a blank stub entry to `blog_posts_meta.json` and populates `blog_posts_content.json` with the HTML body
   - **Important**: The syncer appends a blank meta entry (`_title: ""`, `_show: false`) for any HTML file not already in the content JSON. You must manually fill in the metadata after running it — do not run the syncer again after editing the meta or it will append another blank stub.
4. Edit the stub entry in `src/blog/blog_posts_meta.json` with the correct values:
   ```json
   {
     "_id": "YYYYMMDD_post_slug",
     "_title": "Post Title",
     "_createdAt": "YYYY-MM-DDT00:00:00.000Z",
     "_description": "One-sentence description.",
     "_show": true,
     "_archived": false
   }
   ```
5. Commit changes

**IMPORTANT**: Never directly edit `blog_posts_content.json`. To change blog post content, always edit the source markdown file in `src/blog/content/sources_md/`, then re-run the conversion and sync scripts (steps 2 and 3). The content JSON is a generated artifact and will be overwritten by the syncer.

### Blog Post Images
Images are served via Eleventy passthrough copy, which copies `src/blog/content/images/` to `dist/blog-images/` at build time. The MD-to-HTML converter rewrites `src="images/` to `src="blog-images/"` during conversion.

**To add images to a post:**
1. Create a directory: `src/blog/content/images/<post-slug>/`
2. Place image files in that directory
3. Reference them in your markdown as: `![Alt text](images/<post-slug>/image.png)`
4. The converter handles path rewriting automatically — no manual HTML editing needed

**When copying a post from an external source (e.g. a README from another repo):**
- Image paths must be rewritten from bare filenames (e.g. `![](image.png)`) to the `images/<post-slug>/` convention
- Remove any repo-specific sections (e.g. `## Files` listing notebook/data files) that don't belong on the blog
- Copy all referenced images into the corresponding `src/blog/content/images/<post-slug>/` directory

**To update an existing post's content:**
1. Overwrite the markdown source in `sources_md/`
2. Rewrite image paths to use the `images/<post-slug>/` prefix
3. Remove any repo-specific sections
4. Re-run `01_md_to_html_converter.py` and `02_existing_html_articles_syncer.py`
5. The syncer will update the content JSON without creating a duplicate meta entry

### Adding a New Section
1. Add its content to `src/_data/` (JSON for hand-authored content, a `.js` file if
   anything needs deriving)
2. Create the page template (e.g. `src/newSection.njk`) with `layout:` front matter
3. Add a navigation item to the sidebar partial in `src/_includes/`
4. Add the route to the smoke test's coverage
5. Update this file (`AGENTS.md`)

### Updating Bookshelf
- **Automated**: Trigger `workflow_dispatch` on `sync_bookshelf.yml`
- **Manual**: Run `npm run sync-bookshelf` locally

### Modifying Styles
- Everything compiles from `src/styles/main.scss`; add a partial and `@use` it
- Partials take a leading underscore, which is both the Sass convention and what
  keeps Eleventy from compiling them as pages
- **No animation in this pass** (#501). Static `:hover` / `:focus` states are fine

## Known Issues & Future Work

### Recent Improvements (2025-11-22 to 2025-12-22)
- ✅ Re-enabled ESLint and fixed violations
- ✅ Updated GitHub Actions to latest versions (v4/v5)
- ✅ Fixed Vue 2→3 lifecycle hooks (`beforeDestroy` → `beforeUnmount`)
- ✅ Updated TypeScript shims to Vue 3
- ✅ Removed duplicate ImageCarousel components
- ✅ Standardized all components to use `defineComponent`
- ✅ Added route-level code splitting (lazy loading)
- ✅ Added environment variable validation
- ✅ Replaced DOM queries with Vue template refs
- ✅ Restructured README.md for better developer onboarding

### Completed Features
- **Migrate to Vue 3**: ✅ Done
- **Remove Vue 2 compatibility mode**: ✅ Done
- **Merge Bookshelf-Syncer**: ✅ Done
- **Merge Software-Syncer**: ✅ Done
- **Add Resume & CV PDFs**: ✅ Done

### Planned Work
- **Static rewrite**: in progress on `redesign/static-rewrite`. #545 landed the
  Bio page and #543 (a Work/Education section) was dropped with it: there is no
  such section, and the home page carries no timeline. See #501 for the
  full sub-issue list and the go/no-go checkpoint (#534, #535, #537)
- **Filter blog posts by tag**: Planned
- **Consider moving Blog-Syncer to cloud**: Under consideration
- ~~**Change router to HTML5 mode**~~: obsolete. The rewrite has no router. Real
  nested paths, the hash redirects, `404.html` and the generated sitemap landed
  in #518

### Technical Debt
- No unit tests (only browser smoke tests)
- **There are no scratch TODO files in this repo, by design.** `PROJECT_TODOS.md`,
  `TODO.md`, `GITHUB_ISSUES_TO_CREATE.md`, `dependency_upgrade_todos.md`,
  `scratch_ideas.md` and `plans/` were all deleted: they drifted out of date and
  duplicated the issue tracker. Anything worth doing goes on a GitHub issue
  (see `ISSUES.md`). Do not recreate them

## Blog Writing Style

When writing or editing blog posts for this site, follow these conventions:

### Voice and Tone
- First-person, personal, honest — these are accounts of real experience, not guides or tutorials
- Measured and direct, not flowery or over-written
- Avoid clichéd phrases and filler expressions (e.g. "striking moment", "learned to stay vigilant", "reaching for")
- Don't editorialize or over-explain — let the experience speak for itself
- Show genuine reactions to findings or results ("This one surprised me", "I'm not sure if this is a strength or a limitation"). Opinions and uncertainty are good. Dry reporting is not.
- When tools or automation did the work, say so: "I had Claude Code generate..." not "I generated...". Don't claim personal credit for automated work.

### Content Decisions
- Cut implementation noise that doesn't serve the reader: internal version numbers, zero-count stats, details only a developer would care about. If a number or fact isn't interesting, don't report it.
- Go deep on methodology. Readers want enough process detail to judge whether the approach is sound. Explain the "how" thoroughly, especially when the method is novel or non-obvious.
- Organize around insights, not analysis structure. Each section heading should promise something interesting, not describe a data processing step. "The Model Invents Its Own Pattern Vocabulary" over "Section B: Pattern Analysis".
- When an article is part of a larger system or pipeline, explain the full pipeline briefly before diving into the piece you're analyzing. The reader needs to know where this fits. Keep it self-contained though: don't cross-link to other articles, just say "this article covers X" and move on.
- Every plot needs two things: a brief sentence explaining what the chart shows (axes, colors, groupings), then the insight or takeaway. Don't drop a plot and jump straight to analysis, and don't just describe the data without drawing a conclusion.
- Don't duplicate a chart's data in a table. If the plot shows it, the prose should highlight the insight, not restate the numbers in a different format.
- When discussing limitations, be honest about whether the issue is with the method or with the dataset. "The scale goes unused" could mean the scale is miscalibrated or it could mean the data doesn't have hard enough problems. Name the ambiguity instead of defaulting to self-criticism.

### Punctuation and Formatting
- **No em dashes** — use commas or restructure the sentence instead
- Italics are fine for internal thoughts or emphasis (e.g. *I need to learn how to use this thing*)
- Keep sentences clear and relatively short
- **Always specify a language on markdown code blocks** for syntax highlighting (e.g. ```python, ```bash, ```typescript). If writing pseudocode, use ```python since its highlighting is the closest match.

### Structure
- Personal narrative posts often open with a brief framing paragraph before the main content begins — this sets context (e.g. what series this belongs to, what time period it covers)
- Section headers use the `## Heading` format with a date or phase label where relevant

## AI Assistant Guidelines

### When Making Changes

1. **Read Before Editing**: Always read files before proposing changes
2. **Maintain Conventions**: Follow existing patterns (2-space indent, double quotes)
3. **Preserve Structure**: Keep feature-based directory organization
4. **Update Metadata**: When adding blog posts, update the corresponding JSON files
5. **Test Locally**: Run `npm run lint` and `npm run test:smoke:build` before pushing; suggest `npm run serve` for visual checks
6. **Respect Responsive Design**: One breakpoint, 782px
7. **Compute at Build Time**: Derived values belong in `src/_data/`, not in a template
8. **Global Styles**: Prefer SCSS tokens over hardcoded colors

### When Adding Features

1. **Prefer no JavaScript**: then a little JS, then a partial (#501)
2. **Shared Markup**: Put reusable markup in `src/_includes/`
3. **Pages**: A new page is a new template; its path is its output path
4. **Navigation**: Update the sidebar partial for new nav items
5. **Assets**: Add a passthrough copy entry in `eleventy.config.js`
6. **Data Files**: Follow the patterns in `src/_data/`

### When Debugging

1. **Read the Build Output**: Eleventy names every file it writes; a missing page
   usually means an `ignores` entry or a template format mismatch
2. **Check the Data Layer**: `npx eleventy --to=json` dumps what templates see
3. **Verify Paths**: `require` paths in `src/_data/` are relative to that directory
4. **Build Output**: Check `dist/` after `npm run build`
5. **Image Paths**: Verify paths relative to build output (e.g. `book_thumbnails_v2/`)

### When Refactoring

1. **Backward Compatibility**: Old URLs must keep resolving (#518)
2. **Global Impact**: Check whether an SCSS token change affects other pages
3. **Syncer Contracts**: Never move the JSON files the Python and Actions syncers
   write, and never hand-edit them
4. **JSON Schema**: Maintain consistency in metadata/content JSON files

## Quick Reference

### Important Files to Know
- `eleventy.config.js` - Passthrough copy, Sass compilation, template ignores
- `src/_includes/base.njk` - The HTML shell every page extends
- `src/_data/` - All content and every derived value
- `src/styles/main.scss` - The only compiled stylesheet
- `eslint.config.js` - Lint rules (`npm run lint` gates the deploy)
- `package.json` - Scripts and dependencies

### Common Commands
```bash
npm run serve              # Start dev server
npm run build              # Production build
npm run test:smoke:build   # Build + smoke tests
npm run sync-bookshelf     # Sync Goodreads data
npm run sync-articles      # Sync blog content
```

### Key Directories
- `src/_data/` - Content and derived data
- `src/_includes/` - Layouts and partials
- `src/styles/` - SCSS
- `src/assets/` - Static images and PDFs
- `src/blog/content/` - Blog content pipeline (markdown sources, converted HTML, images)

## Contact & Ownership

- **Owner**: Ben Rombaut
- **Email**: rombaut.benj@gmail.com
- **Website**: [benrombaut.ca](https://www.benrombaut.ca)
- **GitHub**: [@brombaut](https://github.com/brombaut)

---

**Last Updated**: 2026-09-29
**Eleventy Version**: 3.1.6
**Node Version**: 20+ (required by Eleventy and Playwright)
