# Blog Post Local Image Support

## Issue
benrombautca-9zt

## Goal
Enable markdown blog posts to reference local images that get deployed and served from the site, instead of relying on external GitHub raw URLs.

## Design

### Source layout
New directory `src/blog/content/images/` organized by post slug:
```
src/blog/content/images/
  my-post-slug/
    diagram.png
```

### Authoring experience
In markdown source files, reference images with a relative path:
```markdown
![Alt text](images/my-post-slug/diagram.png)
```

### Pipeline changes
1. **CopyPlugin** (`vue.config.js`): Copy `src/blog/content/images/` to `dist/blog-images/`
2. **MD-to-HTML converter** (`01_md_to_html_converter.py`): After Pandoc converts markdown, rewrite `src="images/` to `src="blog-images/` in the HTML output

### Out of scope
- Fixing broken old notebook image URLs (separate task)
- Jupyter notebook image flow

## Active Work
None yet — moving to implementation.

## Completed
- Design approved

## What Didn't Work
(none yet)

## Known Debt / Blockers
- Existing archived posts use absolute GitHub raw URLs pointing to old paths (`src/articles/...`); those are likely broken but not addressed here

## Next Steps
1. Create `src/blog/content/images/` directory with a .gitkeep
2. Add CopyPlugin entry in `vue.config.js`
3. Update `01_md_to_html_converter.py` to rewrite image paths
4. Update CLAUDE.md with image workflow docs
5. Test with a sample image in a post
