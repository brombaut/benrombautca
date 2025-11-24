# Ben Rombaut's Personal Website

[![deploy](https://github.com/brombaut/benrombautca/actions/workflows/gh_pages_deploy.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/gh_pages_deploy.yml)
[![bookshelf-syncer](https://github.com/brombaut/benrombautca/actions/workflows/sync_bookshelf.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/sync_bookshelf.yml)
[![software-syncer](https://github.com/brombaut/benrombautca/actions/workflows/sync_software.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/sync_software.yml)

Personal portfolio website built with Vue 3 and TypeScript. Visit the live site at [benrombaut.ca](https://www.benrombaut.ca).

## Quick Start

### Prerequisites

- **Node.js**: 18+ (check with `node --version`)
- **npm**: 8+ (comes with Node.js)
- **Python**: 3.8+ (for syncing scripts)
- **Pandoc**: For article conversion (optional, only needed for article syncing)

### Installation

```bash
# Clone the repository
git clone https://github.com/brombaut/benrombautca.git
cd benrombautca

# Install dependencies
npm install
```

### Running the Development Server

```bash
npm run serve
```

The site will be available at [http://localhost:8080](http://localhost:8080).

### Building for Production

```bash
npm run build
```

Output files will be in the `dist/` directory.

## Available Scripts

### npm Scripts

| Script | Command | Description |
|--------|---------|-------------|
| **serve** | `npm run serve` | Start development server on localhost:8080 |
| **build** | `npm run build` | Build production-ready bundle to `dist/` directory |
| **lint** | `npm run lint` | Run ESLint (currently disabled) |
| **sync-bookshelf** | `npm run sync-bookshelf` | Sync bookshelf data from Goodreads |
| **sync-articles** | `npm run sync-articles` | Convert Markdown articles to HTML and sync content |

### Shell Scripts

Located in the `scripts/` directory:

| Script | Purpose |
|--------|---------|
| **sync_bookshelf.sh** | Orchestrates Goodreads scraping and bookshelf data syncing |
| **sync_articles.sh** | Converts Markdown articles to HTML using Pandoc |
| **sync_software.sh** | Fetches and converts README files from software projects |
| **deploy.sh** | Manual deployment script (mostly superseded by GitHub Actions) |

### Python Utility Scripts

Image processing utilities in `scripts/`:

- **convert_images_to_webp.py** - Convert images to WebP format
- **reduce_image_size.py** - Optimize image file sizes
- **delete_non_webp_images.py** - Clean up non-WebP image files
- **show_images_size.py** - Report total size of image assets

## Technology Stack

- **Framework**: Vue 3 with TypeScript
- **Build Tool**: Vue CLI 5 (Webpack)
- **Routing**: Vue Router 4 (hash mode)
- **Styling**: SCSS with global variables
- **Icons**: FontAwesome 6
- **Deployment**: GitHub Pages via GitHub Actions

## Site Features

### About Me
Personal introduction with work and education timeline.

### Ben's Bookshelf
Books I've read and am currently reading, synced from [Goodreads](https://www.goodreads.com). Data is scraped and stored using automated syncing pipelines that run via GitHub Actions.

### Articles
Technical how-to guides and notes written in Markdown, converted to HTML using [Pandoc](https://pandoc.org/). Articles cover various programming topics and serve as personal references.

### Software Projects
Showcases README files from my GitHub projects, automatically synced and converted to HTML for display.

### Publications
Academic publications and research papers.

### Running & Hiking
Photo galleries with image carousels showcasing outdoor activities.

## Deployment

The site automatically deploys to GitHub Pages via GitHub Actions:

- **Trigger**: Push to `main` branch or completion of bookshelf sync workflow
- **Workflow**: `.github/workflows/gh_pages_deploy.yml`
- **Target**: `gh-pages` branch
- **Domain**: Custom domain configured via `CNAME` file

### Manual Deployment

```bash
# Build the project first
npm run build

# Deploy using the deploy script (if needed)
bash scripts/deploy.sh
```

## Environment Variables

Required for Firebase integration (bookshelf data). Set these in GitHub Secrets for deployment:

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

For local development, create a `.env` file in the project root with these variables.

## Project Structure

```
benrombautca/
├── src/                    # Source code
│   ├── aboutMe/           # About Me section
│   ├── articles/          # Articles section and content
│   ├── bookshelf/         # Bookshelf with Goodreads sync logic
│   ├── software/          # Software projects section
│   ├── shared/            # Reusable components
│   └── styles/            # Global SCSS styles
├── scripts/               # Utility scripts (sync, image processing)
├── public/                # Static assets
└── .github/workflows/     # CI/CD automation

```

For detailed architecture documentation, see [CLAUDE.md](./CLAUDE.md).

## Development Notes

### Coding Conventions
- **Indentation**: 2 spaces
- **Quotes**: Double quotes
- **TypeScript**: Strict mode enabled
- **Import Alias**: `@/` resolves to `src/`

### Content Syncing

**Articles**: Write in Markdown (`src/articles/content/sources_md/`), run `npm run sync-articles` to convert.

**Bookshelf**: Trigger the GitHub Action or run `npm run sync-bookshelf` locally.

**Software**: GitHub Actions automatically sync README files from specified repositories.

## Future Work

- Filter articles by tag
- Consider moving Article-Syncer to cloud automation
- Switch from hash routing to HTML5 history mode
- Re-enable ESLint and address code quality issues
- Add automated testing

## Contributing

This is a personal portfolio site, but suggestions and bug reports are welcome via GitHub Issues.

## Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Comprehensive AI assistant guide with detailed architecture, patterns, and development workflows
- **[PROJECT_TODOS.md](./PROJECT_TODOS.md)** - Technical debt tracking and improvement opportunities

## License

Copyright © 2025 Ben Rombaut. All rights reserved.

## Contact

- **Website**: [benrombaut.ca](https://www.benrombaut.ca)
- **Email**: rombaut.benj@gmail.com
- **GitHub**: [@brombaut](https://github.com/brombaut)
