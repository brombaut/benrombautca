# TODO - benrombaut.ca

This file tracks potential improvements and tasks for the portfolio website.

## Bookshelf Syncer (`src/bookshelf/syncer_v2/`)

### Bug Fixes
- [ ] Fix author name parsing crash when author name doesn't contain comma (00_goodreads_scraper.py:69, 04_sync_goodreads_with_local.py:44)
  - Currently assumes "Lastname, Firstname" format
  - Will crash on single-name authors or bands
- [ ] Add error handling for page parsing in 04_sync_goodreads_with_local.py:108-115
  - Functions `parse_on_page_from_review_div` and `parse_num_pages_from_review_div` lack try-except blocks
  - Same functions in 00_goodreads_scraper.py have proper error handling
- [ ] Add null check for currently reading books in 04_sync_goodreads_with_local.py:119
  - Will crash if there are no currently reading books
  - 00_goodreads_scraper.py handles this case at line 246-248

### Enhancements
- [ ] Add automated thumbnail downloading for missing books
  - Currently requires manual download
  - Could scrape from Goodreads or use ISBN-based API
- [ ] Add rate limiting/delays to Goodreads scraping
  - Currently only has 1-second delay in 00_goodreads_scraper.py
  - No delays in 04_sync_goodreads_with_local.py
- [ ] Improve logging consistency
  - 00_goodreads_scraper.py has comprehensive logging
  - Other scripts have minimal or no logging
- [ ] Add unit tests for scraping functions
  - Test HTML parsing edge cases
  - Test sync logic for books moving between shelves
- [ ] Add progress indicators for long-running operations
  - Show progress when scraping multiple pages
  - Show conversion progress for images
- [ ] Consider adding a dry-run mode
  - Preview changes before writing to files
  - Useful for debugging sync logic

### Documentation
- [ ] Document the thumbnail naming convention
  - Currently uses `{book_id}.webp`
  - Not immediately clear from code
- [ ] Add docstrings to all functions
  - Especially complex parsing functions
- [ ] Create a README.md in syncer_v2 directory
  - Explain the pipeline flow
  - Document how to manually handle edge cases
  - List dependencies and setup instructions

---

_Last updated: 2025-12-23_
