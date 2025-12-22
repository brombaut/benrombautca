# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**benrombautca** is Ben Rombaut's personal portfolio website, deployed at [benrombaut.ca](https://www.benrombaut.ca). This is a Vue 3 single-page application built with TypeScript, featuring a personal portfolio with multiple sections including About Me, Work/Education timeline, Publications, Articles, Software projects, Bookshelf, Running, and Hiking.

### Tech Stack
- **Framework**: Vue 3 (migrated from Vue 2, using compatibility mode)
- **Language**: TypeScript
- **Build Tool**: Vue CLI 5 with Webpack
- **Routing**: Vue Router 4 (hash mode)
- **Styling**: SCSS with global variables
- **Icons**: FontAwesome (solid, regular, and brands)
- **Deployment**: GitHub Pages
- **Automation**: GitHub Actions

## Repository Structure

```
benrombautca/
├── .github/workflows/          # GitHub Actions workflows
│   ├── gh_pages_deploy.yml    # Main deployment workflow
│   ├── sync_bookshelf.yml     # Bookshelf syncing automation
│   ├── sync_software.yml      # Software projects syncing
│   └── install_lint_build.yml # CI checks
├── public/                     # Static assets
├── scripts/                    # Utility scripts
│   ├── sync_bookshelf.sh      # Local bookshelf sync script
│   ├── sync_articles.sh       # Local articles sync script
│   ├── sync_software.sh       # Local software sync script
│   └── *.py                   # Image processing utilities
├── src/
│   ├── aboutMe/               # About Me section components
│   ├── articles/              # Articles section and content
│   │   └── content/           # Article sources (MD) and converted (HTML)
│   ├── assets/                # Images, resumes, publications PDFs
│   ├── bookshelf/             # Bookshelf section
│   │   └── syncer_v2/         # Goodreads scraping and syncing logic
│   ├── footer/                # Site footer
│   ├── hiking/                # Hiking section with image carousel
│   ├── publications/          # Academic publications section
│   ├── running/               # Running section with image carousel
│   ├── shared/                # Shared/reusable components
│   ├── site-header/           # Navigation and routing
│   ├── software/              # Software projects section
│   ├── styles/                # Global SCSS styles
│   ├── utils/                 # Utility functions
│   ├── workEducation/         # Work and education timeline
│   ├── App.vue                # Root component
│   ├── main.ts                # Application entry point
│   └── app_config.ts          # Feature flags configuration
├── package.json               # Dependencies and scripts
├── tsconfig.json              # TypeScript configuration
├── vue.config.js              # Vue CLI/Webpack configuration
└── babel.config.js            # Babel configuration
```

## Key Architecture Patterns

### Component Structure
Components follow Vue 3 Composition API patterns with TypeScript:

```vue
<template>
  <!-- Template with v-if, v-for, :class bindings -->
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

export default defineComponent({
  name: "ComponentName",
  props: {
    // Typed props
  },
  components: {
    // Child components
  },
  computed: {
    // Computed properties
  },
  methods: {
    // Component methods
  },
  mounted() {
    // Lifecycle hooks
  },
});
</script>

<style lang="scss">
// Scoped or global styles with SCSS
</style>
```

### Routing
- **Mode**: Hash-based routing (`createWebHashHistory`)
- **Router Location**: `src/site-header/router.ts`
- **Dynamic Routes**: Articles and Software sections have dynamic routes (`:articleId`, `:softwareId`)
- **Code Splitting**: All routes use lazy loading (`component: () => import(...)`) for optimal bundle size

### State Management
- **No Vuex/Pinia**: Simple prop passing and component-local state
- **Data Sources**: JSON files imported directly into components
  - `src/articles/authored_articles_meta.json` - Article metadata
  - `src/articles/authored_articles_content.json` - Article HTML content
  - `src/software/software_articles_meta.json` - Software metadata
  - `src/software/software_articles_content.json` - Software README content
  - `src/bookshelf/syncer_v2/all_books_flattened.json` - Bookshelf data

### Shared Components
- **Location**: `src/shared/`
- **Key Components**:
  - `ImageCarousel.vue` - Generic image carousel used by Running and Hiking sections
  - `GitHubMarkdown.vue` - Markdown renderer for articles and software READMEs
  - Other reusable UI components

### Styling System

#### Global Styles
- **Variables**: `src/styles/variables.scss` - Colors, breakpoints, sizes
- **Common**: `src/styles/common.scss` - Shared utility styles
- **Keyframes**: `src/styles/keyframes.scss` - Animation definitions
- **GitHub Article**: `src/styles/github_article.scss` - Markdown rendering styles

#### Color Scheme
- Primary: `#3381db` (benBlue)
- Secondary: `#f1f5fa` (aliceBlue)
- Font: `#33343C` (vsCodeDullBlue)
- Background: `#f1f5fa` (aliceBlue)

#### Responsive Breakpoints
```scss
$MAX_SECTION_SIZE: 1132px;
$MEDIUM_DISPLAY_SIZE: 900px;
$SMALL_DISPLAY_SIZE: 640px;
$TINY_DISPLAY_SIZE: 550px;
$PHONE_DISPLAY_SIZE: 550px;
```

Auto-imported in every component via `vue.config.js`.

## Content Management & Syncing

### Articles
- **Source**: Markdown files in `src/articles/content/sources_md/`
- **Conversion**: Python scripts convert MD → HTML using Pandoc
- **Scripts**:
  - `00_ipynb_to_md_converter.py` - Jupyter notebooks to markdown
  - `01_md_to_html_converter.py` - Markdown to HTML
  - `02_existing_html_articles_syncer.py` - Sync to content JSON
- **Output**: `src/articles/content/converted_html/`
- **Metadata**: Manually maintained in `authored_articles_meta.json`

### Software Projects
- **Source**: README files from external GitHub repositories
- **Sync**: GitHub Actions fetch and convert READMEs
- **Manual Trigger**: `workflow_dispatch` event
- **Metadata**: Manually maintained in `software_articles_meta.json`

### Bookshelf
- **Source**: Goodreads user profile (web scraping)
- **Pipeline**:
  1. `00_goodreads_scraper.py` - Scrapes Goodreads profile
  2. `01_book_thumbnails_copier.py` - Manages book cover images
  3. `02_all_books_flattener.py` - Flattens book data structure
  4. `03_show_missing_thumbnails.py` - Reports missing covers
- **Automation**: GitHub Actions (currently `workflow_dispatch` only, cron commented out)
- **Data**: `src/bookshelf/syncer_v2/all_books_flattened.json`

## Development Workflows

### Local Development

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:8080)
npm run serve

# Build for production
npm run build

# Lint and fix code issues
npm run lint

# Sync bookshelf locally
npm run sync-bookshelf

# Sync articles locally
npm run sync-articles
```

### Environment Variables
Required for Firebase integration (bookshelf data):
```
VUE_APP_API_KEY
VUE_APP_AUTH_DOMAIN
VUE_APP_PROJECT_ID
VUE_APP_STORAGE_BUCKET
VUE_APP_MESSAGING_SENDER_ID
VUE_APP_APP_ID
VUE_APP_MEASUREMENT_ID
VUE_APP_TEST_USER_EMAIL
VUE_APP_TEST_USER_PASSWORD
VUE_APP_FLAG_MARATHON=false
```

Stored in GitHub Secrets for deployment.

### Git Workflow
- **Main Branch**: `main`
- **Deployment**: Automatic on push to `main` via GitHub Actions
- **Protected Branch**: Deploys to `gh-pages` branch

## Coding Conventions

### TypeScript/JavaScript
- **Indentation**: 2 spaces
- **Quotes**: Double quotes (`"`)
- **Semicolons**: Not enforced
- **Max Line Length**: 600 characters (warn only)
- **ESLint**: Based on Vue Essential + Airbnb (many rules disabled for flexibility)

### File Naming
- **Components**: PascalCase (e.g., `BookCard.vue`, `SiteHeader.vue`)
- **Utilities**: kebab-case (e.g., `ui-utils.ts`)
- **Types**: PascalCase (e.g., `types.ts` with PascalCase exports)

### Import Aliases
- `@/` → `src/` (configured in `tsconfig.json` and Webpack)

Example:
```typescript
import BookCard from "@/bookshelf/BookCard.vue";
```

### Component Organization
1. Template
2. Script (imports, component definition, props, computed, methods, lifecycle)
3. Style (SCSS, usually not scoped to allow global variable usage)

## Build & Deployment

### Build Process
```bash
npm run build
```
Outputs to `dist/` directory with:
- Minified JS/CSS bundles
- Copied static assets (CNAME, images, PDFs)
- HTML entry point

### GitHub Actions Deployment
**Workflow**: `.github/workflows/gh_pages_deploy.yml`

Triggers:
- Push to `main` branch
- Completion of `bookshelf-syncer` workflow

Steps:
1. Checkout code
2. Create `.env` file from secrets
3. Install dependencies
4. Run lint (currently no-op)
5. Build project
6. Deploy to `gh-pages` branch

### Static Asset Copying
`vue.config.js` uses `CopyPlugin` to copy:
- `CNAME` → root (for custom domain)
- Book thumbnails → `book_thumbnails_v2/`
- Resumes → `resumes/`
- Publications → `publications/`
- Running images → `running-images/`
- Hiking images → `hiking-images/`

## Testing

**Status**: No automated tests currently configured
- ESLint is enabled and configured with Vue Essential + Airbnb rules
- Test framework not set up (unit/integration/e2e tests planned for future)

## Common Development Tasks

### Adding a New Article
1. Write article in Markdown: `src/articles/content/sources_md/article-name.md`
2. Run conversion script: `python 01_md_to_html_converter.py`
3. Add metadata entry to `src/articles/authored_articles_meta.json`:
   ```json
   {
     "id": "unique-article-id",
     "title": "Article Title",
     "tags": ["tag1", "tag2"],
     "created": "YYYY-MM-DD",
     "updated": "YYYY-MM-DD"
   }
   ```
4. Run sync script: `python 02_existing_html_articles_syncer.py`
5. Commit changes

### Adding a New Section
1. Create directory in `src/` (e.g., `src/newSection/`)
2. Create main section component (e.g., `NewSection.vue`)
3. Add route to `src/site-header/router.ts`
4. Add navigation item to header component
5. Update this CLAUDE.md

### Updating Bookshelf
- **Automated**: Trigger `workflow_dispatch` on `sync_bookshelf.yml`
- **Manual**: Run `npm run sync-bookshelf` locally

### Modifying Styles
- **Global changes**: Edit `src/styles/variables.scss`
- **Component-specific**: Add styles to component's `<style>` block
- **Colors**: Use SCSS variables (`$primary`, `$secondary`, etc.)
- **Breakpoints**: Use provided breakpoint variables for responsive design

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
- **Migrate to Vue 3**: ✅ Done (using compatibility mode)
- **Merge Bookshelf-Syncer**: ✅ Done
- **Merge Software-Syncer**: ✅ Done
- **Add Resume & CV PDFs**: ✅ Done

### Planned Work
- **Filter articles by tag**: Planned
- **Consider moving Article-Syncer to cloud**: Under consideration
- **Change router to HTML5 mode**: TODO (see `router.ts:75`)
- **Remove Vue 2 compatibility mode**: Planned for better performance
- **Add automated testing**: High priority

### Technical Debt
- No automated tests (unit/integration/e2e)
- Some ESLint rules are disabled for flexibility (see `package.json` eslintConfig)
- Vue 2 compatibility mode still enabled (could be removed for better performance)
- Memory leaks in some components (event listeners not cleaned up)
- Heavy use of `any` type in TypeScript (defeats type safety)
- See `PROJECT_TODOS.md` for comprehensive list of improvement opportunities

## AI Assistant Guidelines

### When Making Changes

1. **Read Before Editing**: Always read files before proposing changes
2. **Maintain Conventions**: Follow existing patterns (2-space indent, double quotes)
3. **Preserve Structure**: Keep feature-based directory organization
4. **Update Metadata**: When adding articles/software, update corresponding JSON files
5. **Test Locally**: Suggest running `npm run serve` to verify changes
6. **Respect Responsive Design**: Use existing breakpoint variables
7. **Use Type Safety**: Leverage TypeScript and PropType definitions
8. **Global Styles**: Prefer SCSS variables over hardcoded colors

### When Adding Features

1. **Feature-First Organization**: Create dedicated directories for new major sections
2. **Shared Components**: Put reusable components in `src/shared/`
3. **Route Registration**: Update `router.ts` for new pages
4. **Navigation**: Update header component for new nav items
5. **Assets**: Use `CopyPlugin` in `vue.config.js` for static assets
6. **Data Files**: Follow JSON structure patterns for content management

### When Debugging

1. **Check Browser Console**: Vue Router, component errors appear here
2. **Verify Paths**: Ensure import aliases (`@/`) resolve correctly
3. **SCSS Variables**: Ensure global SCSS is imported (auto-imported via `vue.config.js`)
4. **Build Output**: Check `dist/` after `npm run build`
5. **Image Paths**: Verify paths relative to build output (e.g., `book_thumbnails_v2/`)

### When Refactoring

1. **Backward Compatibility**: Ensure routes and data structures remain compatible
2. **Global Impact**: Check if SCSS variable changes affect other components
3. **TypeScript Types**: Update type definitions when changing data structures
4. **JSON Schema**: Maintain consistency in metadata/content JSON files

## Quick Reference

### Important Files to Know
- `src/main.ts` - Application entry, FontAwesome setup
- `src/App.vue` - Root component with header/footer
- `src/site-header/router.ts` - All route definitions
- `vue.config.js` - Webpack config, asset copying, SCSS auto-import
- `src/styles/variables.scss` - Global color/size variables
- `package.json` - Scripts and dependencies

### Common Commands
```bash
npm run serve              # Start dev server
npm run build              # Production build
npm run sync-bookshelf     # Sync Goodreads data
npm run sync-articles      # Sync article content
```

### Key Directories
- `src/shared/` - Reusable components
- `src/styles/` - Global SCSS
- `src/assets/` - Static images and PDFs
- `src/*/content/` - Content management (articles, software)

## Contact & Ownership

- **Owner**: Ben Rombaut
- **Email**: rombaut.benj@gmail.com
- **Website**: [benrombaut.ca](https://www.benrombaut.ca)
- **GitHub**: [@brombaut](https://github.com/brombaut)

---

**Last Updated**: 2025-12-22
**Vue Version**: 3.2.47
**Node Version**: 18+
**TypeScript Version**: 5.6.3
