# Ben Rombaut's Personal Website

[![deploy](https://github.com/brombaut/benrombautca/actions/workflows/gh_pages_deploy.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/gh_pages_deploy.yml)
[![bookshelf-syncer](https://github.com/brombaut/benrombautca/actions/workflows/sync_bookshelf.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/sync_bookshelf.yml)

Personal portfolio website, built as a framework-free static site with
[Eleventy](https://www.11ty.dev/). Visit the live site at
[benrombaut.ca](https://www.benrombaut.ca).

## Site Features

### About Me
Personal introduction and a News list of recent posts, publications and hikes.

### Bio
Career history in reverse chronological order.

### Ben's Bookshelf
Books I've read and am currently reading, synced from [Goodreads](https://www.goodreads.com). Data is scraped and stored using automated syncing pipelines that run via GitHub Actions.

### Blog
Technical how-to guides and notes written in Markdown, converted to HTML using [Pandoc](https://pandoc.org/). Posts cover various programming topics and serve as personal references.

### Publications
Academic publications and research papers.

### Running & Hiking
Photo galleries showcasing outdoor activities.

## Contributing

This is a personal portfolio site, but suggestions and bug reports are welcome via GitHub Issues.

## Testing

Browser smoke tests load the production build in headless Chromium and fail on any
rendering failure, console error, or broken asset. They cover every section page and
every blog post, the desktop and mobile nav, and the old hash-URL redirects.

```bash
npx playwright install chromium   # one-time
npm run test:smoke:build
```

They also run in CI on every pull request and before each deploy. See `AGENTS.md` for details.

## Documentation

- **[AGENTS.md](./AGENTS.md)** - Comprehensive AI assistant guide with detailed architecture, patterns, and development workflows
- **[CLAUDE.md](./CLAUDE.md)** - Symlink to `AGENTS.md`, so Claude Code reads the same guidance
- **[ISSUES.md](./ISSUES.md)** - GitHub Issues label conventions and the `gh` command reference

## License

Copyright © 2025 Ben Rombaut. All rights reserved.

## Contact

- **Website**: [benrombaut.ca](https://www.benrombaut.ca)
- **Email**: rombaut.benj@gmail.com
- **GitHub**: [@brombaut](https://github.com/brombaut)
