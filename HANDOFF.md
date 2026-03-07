# Handoff Document

## Goal
Rename "articles" to "blog" throughout the entire codebase — routes, component names, file names, directory, data files, Python scripts, docs, and beads issues. Issue: `benrombautca-8xp.2` (in_progress).

## Current Progress
- Issue `benrombautca-8xp.2` is marked `in_progress`
- Research phase complete — all files that need changing have been identified
- No code changes made yet for this rename

### Files Identified (full scope of the rename)

**Directory to rename:**
- `src/articles/` → `src/blog/`

**Vue/TS files inside (rename + update internals):**
- `ArticlesSection.vue` → `BlogSection.vue`
- `SelectedArticleSection.vue` → `SelectedBlogPostSection.vue`
- `AuthoredArticlesProxy.ts` → `BlogPostsProxy.ts`
  - Classes/interfaces: `AuthoredArticlesProxy` → `BlogPostsProxy`, `AuthoredArticleMeta` → `BlogPostMeta`, `AuthoredArticleContent` → `BlogPostContent`, `AuthoredArticle` → `BlogPost`

**JSON data files (rename + update import paths in proxy):**
- `src/articles/authored_articles_meta.json` → `src/blog/blog_posts_meta.json`
- `src/articles/authored_articles_content.json` → `src/blog/blog_posts_content.json`

**Python scripts in `src/articles/content/` (update references, do NOT rename the directory/scripts themselves unless desired):**
- `02_existing_html_articles_syncer.py` — references `authored_articles_meta.json` and `authored_articles_content.json` in default args; update defaults to point to new JSON filenames

**Router (`src/site-header/router.ts`):**
- Path `/articles` → `/blog`, name `articles` → `blog`, import `@/articles/ArticlesSection` → `@/blog/BlogSection`
- Path `/articles/:articleId` → `/blog/:postId`, name `selectedArticle` → `selectedBlogPost`, import `@/articles/SelectedArticleSection` → `@/blog/SelectedBlogPostSection`

**Nav components:**
- `src/site-header/FullNavBar.vue`:
  - ref `articlesNav` → `blogNav`
  - route `/articles` → `/blog`, text `"Articles"` → `"Blog"`
  - `selectedArticle` → `selectedBlogPost` in `getActiveRouteNavElRef()`
- `src/site-header/CondensedNavBar.vue`:
  - path `/articles` → `/blog`, route `articles` → `blog`, label `"Articles"` → `"Blog"`
  - `selectedArticle` → `selectedBlogPost` in `routeIsActive()`
- `src/site-header/NewNavBar.vue`:
  - labels map: `articles: "Articles"` → `blog: "Blog"`, `selectedArticle: "Articles"` → `selectedBlogPost: "Blog"`
  - `isDetailPage`: `routeName === "selectedArticle"` → `routeName === "selectedBlogPost"`
- `src/site-header/BackButton.vue`:
  - `currRouteName === "selectedArticle"` → `currRouteName === "selectedBlogPost"`

**Section header label:**
- `ArticlesSection.vue` (soon `BlogSection.vue`): `title="Articles"` → `title="Blog"`

**CLAUDE.md:**
- Update all references: "Articles" section → "Blog", file paths, workflow docs

**Beads issues:**
- Update descriptions of open issues under `benrombautca-8xp` that reference "articles" terminology

## What Worked
- All prior article-related work (removing tags, updatedAt, redesigning the list, adding archived field) was done cleanly and pushed to main

## What Didn't Work
- N/A — haven't started the rename yet

## Next Steps

1. **Move files**: `git mv src/articles src/blog` to rename the directory (preserves git history), then rename individual files inside with `git mv`
2. **Update `BlogPostsProxy.ts`** (was `AuthoredArticlesProxy.ts`): update JSON import paths, rename all class/interface names
3. **Update `BlogSection.vue`** (was `ArticlesSection.vue`): update imports, component name, section header title, route push name
4. **Update `SelectedBlogPostSection.vue`** (was `SelectedArticleSection.vue`): update imports, route param name, route push name
5. **Update `router.ts`**: paths, names, lazy import paths
6. **Update `FullNavBar.vue`**: ref name, route, text, `getActiveRouteNavElRef` mapping
7. **Update `CondensedNavBar.vue`**: nav item path/route/label, `routeIsActive` cases
8. **Update `NewNavBar.vue`**: labels map, `isDetailPage` condition
9. **Update `BackButton.vue`**: route name check
10. **Update `02_existing_html_articles_syncer.py`**: default arg paths for meta/content JSON
11. **Update `CLAUDE.md`**: all articles → blog references
12. **Update beads issues** with `bd update <id> --description="..."` for any open issues referencing old terminology
13. **Commit and push**, then `bd close benrombautca-8xp.2`
