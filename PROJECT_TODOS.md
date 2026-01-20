# Project TODOs - benrombautca

**Generated:** 2025-11-24
**Active Items:** 34
**Completed Items:** 15
**Won't Do Items:** 6
**Total Items:** 55

This document tracks technical debt, code quality issues, and improvement opportunities identified through a comprehensive codebase audit.

---

## 🟢 SIMPLE (10 items - 1-2 hours each)

### Code Quality

#### 1. Add pre-commit hooks
- **File:** `.husky/pre-commit:4`
- **Issue:** Only runs `setLastDeployed.sh`, no linting or type checking
- **Impact:** Poor code quality can be committed
- **Fix:** Add lint-staged to run ESLint and TypeScript checks

### Performance

#### 2. Add bundle analyzer
- **Issue:** No webpack-bundle-analyzer configured
- **Impact:** No visibility into bundle size and optimization opportunities
- **Fix:** Add `webpack-bundle-analyzer` to dev dependencies

#### 3. Throttle scroll/resize handlers
- **Files:** Multiple components (WorkCard.vue, EducationCard.vue, FullNavBar.vue, BookCard.vue)
- **Issue:** No throttling/debouncing on expensive event handlers
- **Impact:** Performance issues on scroll/resize, especially on mobile
- **Fix:** Add lodash.throttle or lodash.debounce to handlers

### Accessibility

#### 4. Add skip navigation link
- **File:** `src/App.vue`
- **Issue:** No skip-to-main-content link for screen readers
- **Impact:** Screen reader users must tab through navigation every page
- **Fix:** Add skip link at top of App.vue

#### 5. Add keyboard navigation
- **Files:** `src/workEducation/VerticalTimeline.vue:20`, navigation hamburger menu
- **Issue:** Click handlers without keyboard event handlers
- **Impact:** Not accessible via keyboard navigation
- **Fix:** Add @keydown handlers, ensure tabindex is set correctly

#### 6. Audit color contrast
- **File:** `src/styles/variables.scss`
- **Issue:** No accessibility audit documented for color combinations
- **Impact:** May not meet WCAG AA/AAA contrast requirements
- **Fix:** Run axe-core or Lighthouse accessibility audit, fix contrast issues

### SEO & Meta

#### 7. Add meta tags
- **File:** `public/index.html:1-10`
- **Issue:** Missing OpenGraph tags, Twitter Card tags, canonical URLs, structured data (JSON-LD)
- **Impact:** Poor social media sharing, reduced SEO effectiveness
- **Fix:** Add vue-meta or @vueuse/head for dynamic meta tags

#### 8. Add favicon variants
- **File:** `public/` only has `favicon.ico`
- **Issue:** Missing modern favicon formats (PNG, SVG) and sizes for different devices
- **Impact:** Poor appearance on mobile devices and bookmarks
- **Fix:** Add favicon-16x16, favicon-32x32, apple-touch-icon, etc.

### Security

#### 9. Add SRI to third-party scripts
- **File:** `public/index.html:26-30`
- **Issue:** clustrmaps.com script loaded without SRI (Subresource Integrity)
- **Impact:** Potential XSS if CDN is compromised
- **Fix:** Add integrity attribute or remove if not critical

### Miscellaneous

#### 10. Move CSS variables to global
- **File:** `src/bookshelf/BookCard.vue:88-104`
- **Issue:** CSS custom properties defined in Vue component instead of global CSS
- **Impact:** Not reusable across components
- **Fix:** Move to global CSS variables or SCSS variables

---

## 🟡 MEDIUM (23 items - 1-2 days each)

### Vue 3 Migration

#### 11. Remove Vue 2 compatibility mode
- **File:** `vue.config.js:8-22`
- **Issue:** Vue 2 compatibility mode (MODE: 2) is still active despite migration to Vue 3
- **Impact:** Missing out on Vue 3 performance improvements and tree-shaking benefits
- **Fix:** Test with compatConfig MODE: 3, then remove compatibility entirely

#### 12. Update ESLint configuration
- **File:** `package.json:62-103`
- **Issue:** Many important ESLint rules are disabled, including `no-unused-vars: 0`, `no-console: 0`, `no-shadow: 0`, `no-param-reassign: 0`
- **Impact:** Allows poor code practices and potential bugs
- **Fix:** Re-enable critical rules gradually, fix violations

### Type Safety

#### 13. Replace `any` types
- **Files:** `src/main.ts:80`, `src/bookshelf/BookCard.vue:35`, `src/software/SoftwareArticlesProxy.ts:74`, `src/articles/AuthoredArticlesProxy.ts:55` (10+ files total)
- **Issue:** Heavy use of `any` type defeats TypeScript's type safety
- **Impact:** Lost type safety benefits, harder to catch bugs at compile time
- **Fix:** Replace `any` with proper types, especially in component props and return types

#### 14. Enable strict TypeScript flags
- **File:** `tsconfig.json:5`
- **Issue:** Only `strict: true` is set, missing `strictNullChecks`, `strictFunctionTypes`, `noUnusedLocals`, `noUnusedParameters`
- **Impact:** Not maximizing TypeScript's type safety capabilities
- **Fix:** Enable additional strict flags incrementally

#### 15. Document data schemas
- **Issue:** No documentation for data structures and JSON formats
- **Impact:** Hard to understand data flow and structure
- **Fix:** Document JSON schemas for articles, books, software metadata

### Security

#### 16. Configure security headers
- **Issue:** No evidence of security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- **Impact:** Vulnerable to clickjacking, MIME-sniffing attacks
- **Fix:** Configure security headers in GitHub Pages or add _headers file

### Performance & Dependencies

#### 17. Update major dependencies
- **Issue:** FontAwesome packages 6.5.x → 7.1.0, copy-webpack-plugin 11.0.0 → 13.0.1, dotenv 16.6.1 → 17.2.3
- **Impact:** Missing features, security patches, and performance improvements
- **Fix:** Update dependencies incrementally and test

#### 18. Optimize image pipeline
- **File:** `vue.config.js:37-63`
- **Issue:** 2.6MB of book thumbnails copied as-is, no image optimization pipeline
- **Impact:** Slower page loads, higher bandwidth usage
- **Fix:** Add image optimization to build process (imagemin-webpack-plugin)

#### 19. Optimize FontAwesome imports
- **File:** `src/main.ts:1-77`
- **Issue:** Individual icon imports instead of tree-shaking, manually adding each icon
- **Impact:** Larger bundle size than necessary
- **Fix:** Consider using FontAwesome's tree-shakeable packages or SVG sprite approach

### Accessibility

#### 20. Add ARIA attributes
- **Issue:** Only 4 components have any accessibility attributes
- **Impact:** Poor screen reader support, fails WCAG compliance
- **Fix:** Add proper ARIA labels, roles, and semantic HTML throughout

#### 21. Add component documentation
- **Issue:** No JSDoc comments or prop documentation in most components
- **Impact:** Harder for developers to understand component usage
- **Fix:** Add JSDoc comments to all public components and methods

### Architecture & Organization

#### 22. Redesign articles pipeline for better organization
- **Files:** `src/articles/content/`, `scripts/02_existing_html_articles_syncer.py`, `scripts/01_md_to_html_converter.py`, `scripts/00_ipynb_to_md_converter.py`, `vue.config.js`
- **Issue:** Current articles pipeline is disorganized with sources, converted files, and images in separate locations. Each article should have its own directory containing all related assets (source markdown/notebook, images, converted HTML).
- **Impact:**
  - Hard to manage article assets (finding which images belong to which article)
  - Manual process to determine if article is markdown or notebook
  - Unclear how to properly serve article images in dist bundle
  - Poor developer experience when creating/editing articles
- **Fix:**
  - Restructure to `src/articles/content/<article-id>/` directory structure
  - Each article directory contains: source file (`.md` or `.ipynb`), images folder, and generated HTML
  - Update syncer to auto-detect source format (markdown vs notebook) and follow appropriate conversion pipeline
  - Configure webpack CopyPlugin to copy article images to dist
  - Update image paths in conversion scripts to reference article-specific directories
- **Benefits:**
  - Self-contained articles with all assets in one place
  - Easier to add/remove articles (just add/delete a directory)
  - Clear separation of concerns
  - Better scalability as article count grows

#### 23. Extract hardcoded URLs
- **Files:** `src/workEducation/workEntities.ts`, `src/publications/publications.ts`, `src/site-header/SiteHeader.vue` (25+ URLs total)
- **Issue:** URLs hardcoded instead of being in configuration
- **Impact:** Harder to update, no single source of truth
- **Fix:** Extract to configuration file or constants

#### 24. Replace magic numbers
- **File:** `src/bookshelf/BookshelfSection.vue:131-144`
- **Issue:** Hardcoded viewport width thresholds with comment "determined manually by resizing window lol"
- **Impact:** Brittle responsive design, hard to maintain
- **Fix:** Use CSS media queries or standardized breakpoints

#### 25. Use CSS classes over inline styles
- **Files:** `src/shared/GitHubMarkdown.vue:17-22`, `src/site-header/FullNavBar.vue:48-51`, `src/running/ImageCarousel.vue:73-79`
- **Issue:** Setting styles via JavaScript instead of CSS classes
- **Impact:** Harder to maintain, poor separation of concerns
- **Fix:** Use CSS classes with reactive class bindings

#### 26. Add consistent date handling
- **Issue:** Multiple files parse dates differently, no consistent date parsing/formatting library
- **Impact:** Potential timezone and format bugs
- **Fix:** Add date-fns or dayjs for consistent date handling

### SEO & Routing

#### 27. Switch to HTML5 history mode
- **File:** `src/site-header/router.ts:75-77`
- **Issue:** Using hash routing (#/) instead of HTML5 history mode (TODO comment present)
- **Impact:** Search engines may not properly index routes
- **Fix:** Switch to HTML5 history mode, configure server-side routing

#### 28. Document browser support
- **Issue:** No documented browser support policy or testing
- **Impact:** Unknown compatibility with older browsers
- **Fix:** Add Browserstack or document supported browsers

### CI/CD & Deployment

#### 29. Add staging environment
- **Issue:** Deploys directly to production from main branch
- **Impact:** No testing ground for changes before production
- **Fix:** Add staging deployment from develop branch

#### 30. Track bundle size over time
- **Issue:** No tracking of bundle size over time
- **Impact:** Bundle size can grow unnoticed
- **Fix:** Add bundlesize or similar to CI to track size regression

#### 31. Add cross-browser testing
- **Issue:** No browser compatibility testing
- **Impact:** Unknown compatibility issues
- **Fix:** Add Browserstack or similar automated testing

### Bookshelf

#### 32. Redesign bookshelf syncer to optimize Goodreads syncing
- **Files:** `src/bookshelf/syncer_v2/`, `.github/workflows/sync_bookshelf.yml`, bookshelf data JSON files
- **Issue:** Current implementation scrapes all bookshelves (read, currently-reading, to-read) from Goodreads on every sync, causing frequent failures due to web scraping fragility and unnecessary resource usage
- **Impact:**
  - Frequent sync failures due to Goodreads web scraping being brittle
  - Wasted resources re-scraping books that never change (read books are permanent)
  - Poor reliability of bookshelf updates
  - No historical preservation of read books data
- **Fix:** Implement hybrid syncing approach:
  - **Read shelf**: Save all read books once to permanent JSON storage (assumption: books never move out of read shelf once added)
  - **Currently-reading shelf**: Dynamically sync to update reading progress and potentially move books to read shelf when finished
  - **To-read shelf**: Dynamically sync to update book ordering/priorities
  - Update GitHub Actions workflow to support new hybrid sync strategy
  - Add data migration script to initialize permanent read books JSON from current data
- **Benefits:**
  - More reliable syncing (less scraping = fewer failure points)
  - Faster sync times (only updating what actually changes)
  - Permanent storage of read books (historical data preserved)
  - Reduced load on Goodreads servers
  - Better separation of static vs dynamic data

#### 33. Add test coverage reporting
- **Issue:** No test coverage measurement or reporting configured
- **Impact:** No visibility into test coverage (after tests exist)
- **Fix:** Add coverage reporting with Vitest/Istanbul

---

## 🔴 HIGH (1 item - 1+ weeks each)

### Memory & Performance

#### 34. Fix memory leaks systematically
- **Files:** `src/workEducation/WorkCard.vue:61`, `src/workEducation/EducationCard.vue:67`, `src/site-header/FullNavBar.vue:90`, `src/bookshelf/BookCard.vue:80`
- **Issue:** Components add window event listeners but never remove them, causing memory leaks
- **Impact:** Performance degradation over time as users navigate between routes
- **Fix:** Add `beforeUnmount()` lifecycle hooks to clean up listeners in all affected components

---

## 🎯 Recommended Priority Order

For maximum impact with minimal effort:

1. **Add pre-commit hooks** (#1) - Prevent poor code quality from being committed
2. **Throttle scroll/resize handlers** (#3) - Immediate performance improvement
3. **Fix memory leaks** (#34) - Critical for user experience
4. **Remove Vue 2 compatibility mode** (#11) - Unlock Vue 3 performance benefits
5. **Replace `any` types** (#13) - Improve type safety incrementally
6. **Update major dependencies** (#17) - Security patches and improvements

---

## ✅ COMPLETED (15 items)

### Critical Quick Wins

#### Re-enable ESLint
- **File:** `package.json:8`
- **Issue:** Lint script was disabled with `echo Linting Disabled!!!!!!!` instead of running actual linting
- **Impact:** No code quality enforcement, allowing bugs and inconsistencies to slip through
- **Fix:** Re-enable ESLint and address existing violations
- **Status:** ✅ Completed - Lint script now properly configured as `"vue-cli-service lint"`

#### Update GitHub Actions versions
- **Files:** `gh_pages_deploy.yml`, `sync_bookshelf.yml`, `install_lint_build.yml`, `sync_software.yml`
- **Issue:** Using deprecated GitHub Actions v2 (security risk)
- **Impact:** Security vulnerabilities and potential workflow failures
- **Fix:** Update to latest versions (actions/checkout@v4, actions/setup-python@v5, etc.)
- **Status:** ✅ Completed - All GitHub Actions updated to latest stable versions:
  - actions/checkout: v2/v2.3.1 → v4
  - actions/setup-python: v2 → v5
  - actions/setup-node: v2 → v4
  - JamesIves/github-pages-deploy-action: 4.1.4 → v4

#### Fix Vue 2→3 lifecycle hooks
- **Files:** `src/bookshelf/BookshelfSection.vue:157`, `src/shared/GitHubMarkdown.vue:42`
- **Issue:** Using deprecated `beforeDestroy` instead of Vue 3's `beforeUnmount`
- **Impact:** Will break when Vue 2 compatibility is removed
- **Fix:** Replace all `beforeDestroy` with `beforeUnmount`
- **Status:** ✅ Completed - All `beforeDestroy` hooks replaced with `beforeUnmount`

#### Update TypeScript shims
- **Files:** `src/shims-vue.d.ts:2`, `src/shims-tsx.d.ts:1`
- **Issue:** Type declarations import from Vue 2 (`import Vue from "vue"`)
- **Impact:** Incorrect type information in IDE
- **Fix:** Update to use Vue 3 types
- **Status:** ✅ Completed - Both shim files updated to use Vue 3 type definitions

### Code Quality

#### Remove duplicate ImageCarousel
- **Files:** `src/running/ImageCarousel.vue`, `src/hiking/ImageCarousel.vue`
- **Issue:** Identical carousel component duplicated (only difference is type import)
- **Impact:** Code duplication, harder to maintain
- **Fix:** Extract to `src/shared/ImageCarousel.vue` with generic typing
- **Status:** ✅ Completed - Created shared ImageCarousel component with generic CarouselImage interface, updated both RunningCard and HikingCard to use shared component, removed duplicates

#### Standardize component definitions
- **Files:** `src/App.vue`, `src/workEducation/WorkEducationSection.vue`
- **Issue:** 2 components use plain `export default {}`, 40 use `defineComponent`
- **Impact:** Inconsistent codebase
- **Fix:** Convert all to `defineComponent` for consistency
- **Status:** ✅ Completed - Both components now use `defineComponent`

#### Remove commented code
- **Files:** `src/site-header/SiteHeader.vue:34-37`, `src/site-header/FullNavBar.vue:10`, `src/shared/GitHubMarkdown.vue:35`
- **Issue:** Commented code left in production codebase
- **Impact:** Code clutter, confusion about what's active
- **Fix:** Remove commented code, use feature flags if needed
- **Status:** ✅ Completed - All commented code removed from production files

#### Track TODO comments
- **Files:** `src/articles/ArticlesSection.vue:54`, `src/site-header/router.ts:75`, `src/site-header/SiteHeader.vue:57`, `src/workEducation/VerticalTimeline.vue:108`, `src/site-header/NewNavBar.vue:48`, `src/bookshelf/BookshelfSection.vue:79`
- **Issue:** 6 TODO comments without associated issues or tracking
- **Impact:** Technical debt not visible or prioritized
- **Fix:** Convert TODOs to GitHub issues
- **Status:** ✅ Completed - All TODO comments documented and prepared as GitHub issues in GITHUB_ISSUES_TO_CREATE.md (5 issues total - one TODO was already removed)

#### Remove unused properties
- **Files:** `src/bookshelf/BookshelfSection.vue:79`, `src/articles/ArticlesSection.vue:42`
- **Issue:** `booksLoading` always false, `selectedArticle` never used
- **Impact:** Dead code, larger bundle
- **Fix:** Remove unused properties or implement features
- **Status:** ✅ Completed - Removed `booksLoading` property and loader UI from BookshelfSection, removed `selectedArticle` from ArticlesSection

#### Replace DOM queries with refs
- **Files:** `src/workEducation/VerticalTimeline.vue:83-88`, `src/running/ImageCarousel.vue:64-79`
- **Issue:** Using `querySelector` instead of Vue template refs
- **Impact:** Less Vue-idiomatic, harder to track reactivity
- **Fix:** Use template refs ($refs) instead of querySelector
- **Status:** ✅ Completed - Replaced querySelector/getElementsByClassName with Vue template refs in both components

#### Fix Husky path
- **File:** `.husky/pre-commit:4`
- **Issue:** References `./setLastDeployed.sh` with relative path
- **Impact:** May fail if run from subdirectories
- **Fix:** Use absolute path or proper directory resolution
- **Status:** ✅ Completed - Updated pre-commit hook to use `$(git rev-parse --show-toplevel)` for reliable path resolution from any directory

### Performance

#### Add route-level code splitting
- **File:** `src/site-header/router.ts`
- **Issue:** All routes import components synchronously, no lazy loading
- **Impact:** Larger initial bundle size, slower first load
- **Fix:** Convert route components to lazy imports: `component: () => import(...)`
- **Status:** ✅ Completed - Converted all route component imports to lazy-loaded dynamic imports. Also updated tsconfig.json module setting from "es2015" to "esnext" to support dynamic imports. Build successful with separate chunks for each route component.

### SEO & Meta

#### Generate sitemap.xml
- **Issue:** Missing sitemap for search engine crawlers
- **Impact:** Reduced discoverability by search engines
- **Fix:** Generate sitemap.xml and robots.txt, add to public folder
- **Status:** ✅ Completed - Created sitemap.xml with all static and dynamic routes (10 main pages, 29 articles, 4 software projects) and robots.txt file in public/ directory. Files are automatically copied to dist/ during build and will be deployed to site root.

### Security

#### Validate environment variables
- **File:** `src/app_config.ts:1-3`
- **Issue:** Environment variables used without validation or fallbacks
- **Impact:** Silent failures if env vars missing
- **Fix:** Add runtime validation for required env vars
- **Status:** ✅ Completed - Added comprehensive validation system with:
  - Runtime validation for required environment variables
  - Warnings for invalid optional variables
  - Helper functions for type-safe boolean env var parsing
  - Automatic validation on module load with clear error messages
  - Development-mode warnings for configuration issues

### Documentation

#### Update README.md
- **Files:** `README.md`, `CLAUDE.md`
- **Issue:** README still mentions "Migrate to Vue 3" as future work, but CLAUDE.md says it's done
- **Impact:** Confusing documentation, outdated information
- **Fix:** Update README.md to reflect current state
- **Status:** ✅ Completed - README.md updated to reflect Vue 3 migration completion

#### Restructure README.md for practical developer onboarding
- **File:** `README.md`
- **Issue:** README focuses heavily on project source code structure but lacks practical information for getting started: dev environment setup steps, production build instructions, and comprehensive list of available scripts (both npm scripts and shell scripts like `sync_bookshelf.sh`, `set_last_deployed.sh`, etc.)
- **Impact:** New developers (or returning after time away) have to hunt through multiple files to understand how to run the project
- **Fix:** Restructure README to prioritize:
  - Development environment setup (prerequisites, installation steps)
  - Running the dev server
  - Building for production
  - Available npm scripts with descriptions
  - Available shell scripts in `/scripts` directory with usage
  - Move detailed source code structure to CLAUDE.md or separate ARCHITECTURE.md
- **Status:** ✅ Completed - README.md completely restructured with Quick Start section, comprehensive script documentation, environment setup, and deployment information

---

## 🚫 WON'T DO (6 items)

### Documentation

#### Add CONTRIBUTING.md
- **Issue:** No CONTRIBUTING.md file
- **Impact:** Contributors don't know how to help
- **Reason:** Personal portfolio site - not accepting external contributions

#### Document rollback procedure
- **Issue:** No documented rollback procedure
- **Impact:** Difficult to recover from bad deployments
- **Reason:** GitHub Pages deployment history provides sufficient rollback capability via git

### Miscellaneous

#### Uncomment cron schedule
- **File:** `.github/workflows/sync_bookshelf.yml:3-6`
- **Issue:** Automated bookshelf sync cron job is commented out
- **Impact:** Manual intervention required, doesn't auto-sync
- **Reason:** Prefer manual control over bookshelf syncing to review changes before deployment

### Error Handling & Security

#### Add error boundaries
- **Issue:** Only 2 files use try/catch (`src/hiking/hikes.ts`, `src/running/races.ts`)
- **Impact:** Poor user experience when errors occur, difficult debugging
- **Reason:** Static content site with minimal dynamic behavior - errors are rare and acceptable to surface directly

#### Sanitize v-html content
- **Files:** `src/shared/GitHubMarkdown.vue:4`, `src/aboutMe/AboutMeSection.vue:11`, `src/hiking/HikingCard.vue:14`, `src/running/RunningCard.vue:12,16,18`
- **Issue:** Using `v-html` without sanitization on user/external content
- **Impact:** Potential XSS attacks if content sources are compromised
- **Reason:** All content is self-authored and controlled - no untrusted external sources

#### Implement CSP headers
- **Issue:** No Content Security Policy headers configured
- **Impact:** Vulnerable to XSS and injection attacks
- **Reason:** GitHub Pages does not support custom headers; static site with controlled content sources provides sufficient security

---

## Progress Tracking

### Active TODOs
- [ ] Simple: 10 items remaining
- [ ] Medium: 23 items remaining
- [ ] High: 1 item remaining
- **Total Active: 34 items**

### Completed
- ✅ 15 items completed (see Completed section above)

### Won't Do
- 🚫 6 items (see Won't Do section above)

### Overall Statistics
- **Active:** 34 items (61.8%)
- **Completed:** 15 items (27.3%)
- **Won't Do:** 6 items (10.9%)
- **Total:** 55 items

---

**Note:** This list represents a comprehensive audit. Not all items need to be completed immediately. Prioritize based on project goals and user impact.
