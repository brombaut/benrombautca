# GitHub Issues to Create for TODO Comments

This document contains all the GitHub issues that should be created to track TODO comments found in the codebase (PROJECT_TODOS.md #9).

---

## Issue 1: ArticlesSection - Decide whether to use or remove listOfUniqueTags feature

**Title:** `ArticlesSection: Decide whether to use or remove listOfUniqueTags feature`

**Labels:** `tech-debt`, `code-quality`

**Body:**
```markdown
## Description
There is a TODO comment in `src/articles/ArticlesSection.vue:53` indicating that the `listOfUniqueTags` computed property needs to be either used or removed.

## Current State
The `listOfUniqueTags` computed property calculates tag counts from articles but is not currently being used in the component template.

## Location
File: `src/articles/ArticlesSection.vue:53`

```typescript
listOfUniqueTags(): string[] {
  // TODO: Use it or remove it
  const arrayOfTagsArrays: string[][] = this.authoredArticles.map((aa: AuthoredArticle) => aa.tags);
  type TagCount = {
    tag: string,
    count: number
  };
  const result: TagCount[] = [];
  // ... rest of implementation
}
```

## Possible Actions
1. **Use it**: Implement article filtering by tags in the UI (aligns with README future work)
2. **Remove it**: Delete the unused computed property to reduce code clutter

## Context
This relates to a broader feature request mentioned in the README about implementing article tag filtering.

## Related
- PROJECT_TODOS.md #9: Track TODO comments
```

---

## Issue 2: Router - Migrate from hash mode to HTML5 history mode

**Title:** `Router: Migrate from hash mode to HTML5 history mode for better SEO`

**Labels:** `enhancement`, `SEO`, `routing`

**Body:**
```markdown
## Description
There is a TODO comment in `src/site-header/router.ts:75` suggesting to migrate from hash-based routing to HTML5 history mode.

## Current State
The application currently uses hash-based routing (`createWebHashHistory`), which results in URLs with `#/` (e.g., `https://benrombaut.ca/#/articles`).

## Location
File: `src/site-header/router.ts:75`

```typescript
// TODO: Maybe change this to html5 - https://router.vuejs.org/guide/essentials/history-mode.html
const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});
```

## Benefits of HTML5 History Mode
- Better SEO: Search engines may not properly index routes with hash fragments
- Cleaner URLs: `/articles` instead of `/#/articles`
- More professional appearance

## Implementation Considerations
1. Change `createWebHashHistory` to `createWebHistory`
2. Configure GitHub Pages to redirect all routes to `index.html` (create a `404.html` that redirects)
3. Test all routes to ensure they work correctly with direct navigation
4. Update any hardcoded links that assume hash routing

## References
- [Vue Router HTML5 History Mode Guide](https://router.vuejs.org/guide/essentials/history-mode.html)
- [GitHub Pages SPA routing solutions](https://github.com/rafgraph/spa-github-pages)

## Related
- PROJECT_TODOS.md #9: Track TODO comments
- PROJECT_TODOS.md #47: Switch to HTML5 history mode
```

---

## Issue 3: SiteHeader - Use dynamic navbar height instead of hardcoded margin

**Title:** `SiteHeader: Calculate navbar height dynamically instead of using hardcoded margin`

**Labels:** `tech-debt`, `refactoring`, `responsive-design`

**Body:**
```markdown
## Description
There is a TODO comment in `src/site-header/SiteHeader.vue:53` indicating that the bottom margin should query the navbar height dynamically instead of using a hardcoded value.

## Current State
The bottom margin is hardcoded to `42px` with a comment noting it matches the navbar height.

## Location
File: `src/site-header/SiteHeader.vue:53`

```scss
.bottom-margin {
  margin-bottom: 42px; // Hight of the navbar - TODO: Change this to query the nav height and set the bottom maring style
}
```

## Problem
- Hardcoded values are brittle and break when navbar height changes
- Different screen sizes might have different navbar heights
- Typo: "maring" should be "margin"

## Proposed Solution
1. Query the navbar height using JavaScript/TypeScript
2. Set the margin dynamically using computed styles or CSS custom properties
3. Consider using CSS `position: sticky` if applicable

## Implementation Options

**Option A: Vue refs and computed styles**
```typescript
computed: {
  navbarHeight(): number {
    return (this.$refs.navbar as HTMLElement)?.offsetHeight || 42;
  }
}
```

**Option B: CSS custom properties**
```typescript
mounted() {
  const navHeight = this.$el.querySelector('.navbar').offsetHeight;
  document.documentElement.style.setProperty('--navbar-height', `${navHeight}px`);
}
```

```scss
.bottom-margin {
  margin-bottom: var(--navbar-height, 42px);
}
```

## Related
- PROJECT_TODOS.md #9: Track TODO comments
- PROJECT_TODOS.md #11: Replace DOM queries with refs
```

---

## Issue 4: VerticalTimeline - Remove or use TINY_PHONE_RARELY_USED_SIZE media query

**Title:** `VerticalTimeline: Decide whether to use or remove TINY_PHONE_RARELY_USED_SIZE breakpoint`

**Labels:** `tech-debt`, `responsive-design`, `code-quality`

**Body:**
```markdown
## Description
There are TODO comments in both `src/workEducation/VerticalTimeline.vue:108` and `src/styles/variables.scss:33` questioning whether the `TINY_PHONE_RARELY_USED_SIZE` breakpoint should be used.

## Current State
A media query for extremely small screens (300px) exists but has a TODO comment questioning its necessity.

## Locations

**File 1:** `src/workEducation/VerticalTimeline.vue:108`
```scss
// TODO: Should this be used?
@media screen and (max-width: $TINY_PHONE_RARELY_USED_SIZE) {
  min-width: 150px;
}
```

**File 2:** `src/styles/variables.scss:33`
```scss
// TODO: Try to remove this - its only used in the verticalTimeline
$TINY_PHONE_RARELY_USED_SIZE: 300px;
```

## Analysis Needed
1. **Usage statistics**: Check analytics to see if any visitors have screens < 300px wide
2. **Modern device landscape**: Most modern phones are >= 320px wide
3. **Testing**: Test the timeline on 320px width to see if the current breakpoints are sufficient

## Possible Actions
1. **Remove it**: Delete the media query and SCSS variable if analytics show no usage
2. **Keep it**: If there's measurable traffic from very small screens, document why it's needed
3. **Simplify**: Merge with existing `$TINY_DISPLAY_SIZE` (550px) if the distinction isn't meaningful

## Related
- PROJECT_TODOS.md #9: Track TODO comments
- PROJECT_TODOS.md #44: Replace magic numbers
```

---

## Issue 5: NewNavBar - Fix type conversions in watchStickyNav method

**Title:** `NewNavBar: Improve type safety in watchStickyNav method by fixing type conversions`

**Labels:** `typescript`, `tech-debt`, `type-safety`

**Body:**
```markdown
## Description
There is a TODO comment in `src/site-header/NewNavBar.vue:48` indicating that the type conversions in the `watchStickyNav` method need to be fixed.

## Current State
The method uses `as unknown as SiteHeader` to cast `this.$parent`, which bypasses TypeScript's type checking.

## Location
File: `src/site-header/NewNavBar.vue:48`

```typescript
watchStickyNav(): void {
  // TODO: Fix these type conversions
  if (window.pageYOffset >= this.startingNavBarOffset) {
    this.$el.classList.add("sticky");
    (this.$parent as unknown as SiteHeader).addBottomMargin();
  } else {
    this.$el.classList.remove("sticky");
    (this.$parent as unknown as SiteHeader).removeBottomMargin();
  }
}
```

## Problem
- Double casting `as unknown as SiteHeader` is a TypeScript anti-pattern
- Loses type safety benefits
- Indicates architectural issue with parent-child communication

## Proposed Solutions

**Option A: Emit events instead of calling parent methods directly**
```typescript
// In NewNavBar.vue
watchStickyNav(): void {
  if (window.pageYOffset >= this.startingNavBarOffset) {
    this.$el.classList.add("sticky");
    this.$emit('sticky-state-changed', true);
  } else {
    this.$el.classList.remove("sticky");
    this.$emit('sticky-state-changed', false);
  }
}

// In SiteHeader.vue
<NewNavBar @sticky-state-changed="handleStickyStateChanged" />
```

**Option B: Use provide/inject for type-safe parent access**
```typescript
// In SiteHeader.vue
provide() {
  return {
    siteHeader: this as SiteHeader
  }
}

// In NewNavBar.vue
inject: ['siteHeader'],
```

**Option C: Properly type the parent component**
```typescript
import type SiteHeader from './SiteHeader.vue';

watchStickyNav(): void {
  const parent = this.$parent as InstanceType<typeof SiteHeader>;
  if (parent && typeof parent.addBottomMargin === 'function') {
    // ... safe to call methods
  }
}
```

## Recommended Approach
Option A (emit events) is the most Vue-idiomatic and provides the best separation of concerns.

## Related
- PROJECT_TODOS.md #9: Track TODO comments
- PROJECT_TODOS.md #31: Replace `any` types
- PROJECT_TODOS.md #32: Enable strict TypeScript flags
```

---

## Summary

**Total Issues to Create:** 5

**Issue Categories:**
- Code Quality / Tech Debt: 3 issues (#1, #3, #4)
- Enhancement: 1 issue (#2)
- TypeScript / Type Safety: 1 issue (#5)

**Next Steps:**
1. Create these issues in the GitHub repository
2. Apply appropriate labels to each issue
3. Consider adding them to a project board or milestone
4. Update TODO comments in code to reference the GitHub issue numbers
5. Mark PROJECT_TODOS.md #9 as completed

**Note:** Issue #6 from the original list (BookshelfSection.vue TODO) was not found in the current codebase and appears to have been already addressed.
