# Ben Rombaut's Personal Website

[![deploy](https://github.com/brombaut/benrombautca/actions/workflows/gh_pages_deploy.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/gh_pages_deploy.yml)
[![bookshelf-syncer](https://github.com/brombaut/benrombautca/actions/workflows/sync_bookshelf.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/sync_bookshelf.yml)

Personal portfolio website, built as a framework-free static site with
[Eleventy](https://www.11ty.dev/). Visit the live site at
[benrombaut.ca](https://www.benrombaut.ca).

> **This branch is mid-rewrite.** `redesign/static-rewrite` is replacing the
> Vue 3 SPA that still runs on `main`. See issue #501 for the plan and
> `AGENTS.md` for the current state of the build.

## Site Features

### About Me
Personal introduction with work and education timeline.

### Ben's Bookshelf
Books I've read and am currently reading, synced from [Goodreads](https://www.goodreads.com). Data is scraped and stored using automated syncing pipelines that run via GitHub Actions.

### Articles
Technical how-to guides and notes written in Markdown, converted to HTML using [Pandoc](https://pandoc.org/). Articles cover various programming topics and serve as personal references.

### Publications
Academic publications and research papers.

### Running & Hiking
Photo galleries with image carousels showcasing outdoor activities.

## Contributing

This is a personal portfolio site, but suggestions and bug reports are welcome via GitHub Issues.

## Testing

Browser smoke tests load the production build in headless Chromium and fail on any
rendering failure, console error, or broken asset. Coverage is reduced to the pages
the rewrite currently builds; issue #544 restores the full route matrix and adds
screenshot baselines.

```bash
npx playwright install chromium   # one-time
npm run test:smoke:build
```

They also run in CI on every pull request and before each deploy. See `AGENTS.md` for details.

## Documentation

- **[AGENTS.md](./AGENTS.md)** - Comprehensive AI assistant guide with detailed architecture, patterns, and development workflows
- **[CLAUDE.md](./CLAUDE.md)** - Symlink to `AGENTS.md`, so Claude Code reads the same guidance
- **[PROJECT_TODOS.md](./PROJECT_TODOS.md)** - Technical debt tracking and improvement opportunities

## License

Copyright © 2025 Ben Rombaut. All rights reserved.

## Contact

- **Website**: [benrombaut.ca](https://www.benrombaut.ca)
- **Email**: rombaut.benj@gmail.com
- **GitHub**: [@brombaut](https://github.com/brombaut)
