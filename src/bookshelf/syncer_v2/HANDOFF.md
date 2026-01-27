# Bookshelf Syncer Migration to Playwright

## Overview

This document describes the migration from the legacy `requests`-based Goodreads scraper to a new Playwright-based scraper that handles authentication.

**Date**: January 27, 2026
**Reason**: Goodreads now requires authentication to view user bookshelves. The old scraper was being redirected to sign-in pages.

---

## Changes Made

### 1. Files Added

#### `00_goodreads_scraper_playwright.py` (New Scraper)
- **Purpose**: Replacement for the legacy scraper with authentication support
- **Technology**: Playwright (headless browser automation)
- **Authentication**: Email/password login through Amazon's auth portal
- **Output**: Same JSON format as legacy scraper (`all_books.json`)

**Key Features**:
- Automated login to Goodreads via email/password
- CAPTCHA detection with immediate failure (requires manual intervention)
- Error screenshots saved on failures for debugging
- Reuses all existing parsing logic from legacy scraper
- Same output format ensures compatibility with downstream pipeline

#### `.env.example`
- Template for local development credentials
- Shows required environment variables
- Never contains actual credentials (safe to commit)

### 2. Files Modified

#### `requirements.txt`
**Added**:
```
playwright==1.49.1
python-dotenv==1.0.1
```

These enable browser automation and environment variable loading.

#### `.gitignore`
**Added**:
```
src/bookshelf/syncer_v2/.env
src/bookshelf/syncer_v2/credentials.env
```

Prevents accidental credential commits.

#### `.github/workflows/sync_bookshelf.yml`
**Changes**:
- Added Playwright browser installation: `python3 -m playwright install chromium --with-deps`
- Changed script execution from `00_goodreads_scraper.py` → `00_goodreads_scraper_playwright.py`
- Added environment variables for credentials:
  - `GOODREADS_EMAIL`
  - `GOODREADS_PASSWORD`
  - `GOODREADS_USER_ID`

### 3. Files Renamed

- `00_goodreads_scraper.py` → `00_goodreads_scraper_legacy.py`
- Kept for reference and potential rollback
- Can be removed after several months of successful Playwright runs

### 4. Files Unchanged

- `02_all_books_flattener.py` - Uses same input format
- `03_show_missing_thumbnails.py` - Uses same data
- `all_books.json` - Same output structure
- `all_books_flattened.json` - Same output structure

---

## How Authentication Works

### Login Flow

1. Navigate to `https://www.goodreads.com/user/sign_in`
2. Click "Sign in with email" button
3. Redirected to Amazon's auth portal (`/ap/signin`)
4. Enter email and password
5. Amazon redirects back to Goodreads
6. Verify authentication successful
7. Scrape authenticated shelf pages

### Error Handling

**CAPTCHA Detection**:
- If CAPTCHA is detected → **FAILS IMMEDIATELY**
- Saves screenshot (`error_captcha.png` or `error_captcha_amazon.png`)
- Requires manual intervention

**Authentication Failures**:
- Wrong credentials → Error message + screenshot (`error_auth_failed.png`)
- Timeout → Screenshot (`error_timeout.png`)
- Session expiration during scraping → Error message

**Shelf Scraping Errors**:
- Timeout loading page → Screenshot (`error_shelf_{shelf}_page{num}.png`)
- Redirected to sign-in → Session expired error

---

## Testing Guide

### Local Testing (Recommended Before Deployment)

#### Step 1: Set Up Environment

```bash
cd src/bookshelf/syncer_v2

# Create .env file from template
cp .env.example .env
```

#### Step 2: Add Credentials

Edit `.env` and add your actual Goodreads credentials:

```bash
GOODREADS_EMAIL=your.email@example.com
GOODREADS_PASSWORD=your_actual_password
GOODREADS_USER_ID=115130270-ben-rombaut
```

**Important**: Never commit the `.env` file!

#### Step 3: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers (required!)
python3 -m playwright install chromium
```

#### Step 4: Run the Scraper

```bash
python3 00_goodreads_scraper_playwright.py
```

**Expected Output**:
```
[timestamp] - __main__ - INFO - [main] Starting Goodreads scraper with Playwright
[timestamp] - __main__ - INFO - [main] Launching browser
[timestamp] - __main__ - INFO - [authenticate_goodreads] Starting authentication process
[timestamp] - __main__ - INFO - [authenticate_goodreads] Authentication successful!
[timestamp] - __main__ - INFO - [main] Scraping read books
[timestamp] - __main__ - INFO - [main] Scraping to-read books
[timestamp] - __main__ - INFO - [main] Scraping currently reading books
[timestamp] - __main__ - INFO - [main] Scraping completed successfully!
[timestamp] - __main__ - INFO - [main] Total books - Read: X, To-read: Y, Currently reading: Z
```

#### Step 5: Verify Output

```bash
# Check JSON structure
cat all_books.json | head -50

# Check book counts
cat all_books.json | jq '.toread_books | length'
cat all_books.json | jq '.read_books | length'
cat all_books.json | jq '.currentlyreading_books | length'

# Run rest of pipeline
python3 02_all_books_flattener.py
python3 03_show_missing_thumbnails.py
```

#### Step 6: Verify Output Format

The `all_books.json` structure should match:

```json
{
  "toread_books": [
    {
      "title": "Book Title",
      "author": "Author Name",
      "book_id": "12345-book-slug",
      "review_id": 123456789,
      "date_added": "Jan 06, 2026",
      "position": 45
    }
  ],
  "currentlyreading_books": [
    {
      "title": "Book Title",
      "author": "Author Name",
      "book_id": "12345-book-slug",
      "review_id": 123456789,
      "date_added": "Jan 06, 2026",
      "onPage": 50,
      "numPages": 300
    }
  ],
  "read_books": [
    {
      "title": "Book Title",
      "author": "Author Name",
      "book_id": "12345-book-slug",
      "review_id": "123456789",
      "date_finished": "Apr 06, 2025",
      "rating": 4
    }
  ]
}
```

---

## GitHub Actions Deployment

### Step 1: Add GitHub Secrets

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets:

| Secret Name | Value | Required? |
|-------------|-------|-----------|
| `GOODREADS_EMAIL` | Your Goodreads email | Yes |
| `GOODREADS_PASSWORD` | Your Goodreads password | Yes |
| `GOODREADS_USER_ID` | `115130270-ben-rombaut` | Optional (hardcoded default) |

**Security Notes**:
- GitHub automatically masks these values in logs
- Never log credentials in the scraper code
- Secrets are encrypted at rest

### Step 2: Test the Workflow

1. Go to **Actions** tab in GitHub repository
2. Select **bookshelf-syncer** workflow
3. Click **Run workflow** dropdown
4. Select branch (usually `main`)
5. Click **Run workflow**

### Step 3: Monitor Execution

Watch the workflow logs for:

✅ **Success Indicators**:
- `Install Playwright browsers` step completes
- `Run 00_goodreads_scraper_playwright.py` shows "Authentication successful!"
- Books counts printed: `Total books - Read: X, To-read: Y, Currently reading: Z`
- `Commit and push changes` completes (or "nothing to commit" if no changes)

❌ **Failure Indicators**:
- `CAPTCHA detected` - Goodreads is challenging the login (manual intervention needed)
- `Authentication failed` - Check credentials in GitHub Secrets
- `Timeout` - Network issues or slow page loads
- `Session expired` - Session lost during scraping (rare)

### Step 4: Verify Results

After successful workflow run:

1. Check the commit history for "Sync Bookshelf - Automated update from GitHub Action"
2. Inspect `all_books.json` and `all_books_flattened.json` changes
3. Verify book counts match expectations

---

## Troubleshooting

### CAPTCHA Errors

**Symptom**:
```
Exception: CAPTCHA detected - manual intervention required
```

**Solution**:
- CAPTCHAs require human intervention
- Manually log into Goodreads from your IP to "train" the system
- Try running the workflow again
- If persistent, may need to run scraper manually from a trusted IP

**Prevention**:
- Don't run the workflow too frequently (rate limiting)
- Keep existing 1-second delays between pages

### Authentication Failures

**Symptom**:
```
Exception: Authentication failed - verify credentials are correct
```

**Solutions**:
1. Verify `GOODREADS_EMAIL` and `GOODREADS_PASSWORD` secrets are correct
2. Try logging in manually to confirm credentials work
3. Check if Goodreads requires 2FA (not currently supported)
4. Look for `error_auth_failed.png` screenshot (if running locally)

### Session Expiration

**Symptom**:
```
Exception: Session expired - re-authentication needed
```

**Solution**:
- Rarely happens, but if scraping takes too long, session may expire
- Re-run the workflow (fresh login each time)
- Consider reducing scraping scope if this persists

### Missing Books / Empty Shelves

**Symptom**: JSON has empty arrays or fewer books than expected

**Solutions**:
1. Check if selectors changed (Goodreads updated their HTML)
2. Verify authentication worked (check logs for "Authentication successful")
3. Check `parse_*_books_from_html` functions for parsing errors
4. Compare HTML structure with legacy scraper expectations

### Browser Installation Errors (GitHub Actions)

**Symptom**:
```
Error: Browser executable doesn't exist
```

**Solution**:
- Workflow should run `python3 -m playwright install chromium --with-deps`
- The `--with-deps` flag installs system dependencies (required on Ubuntu)
- Check workflow YAML has this step before running the scraper

---

## Next Steps

### Immediate (Required for Production)

- [ ] **Test locally** with your credentials (Phase 3)
- [ ] **Add GitHub Secrets** to repository settings (Phase 5)
- [ ] **Run workflow manually** and verify success (Phase 5)
- [ ] **Monitor first few runs** for stability

### Optional Improvements

- [ ] **Enable cron schedule** after confirming stability (uncomment in `sync_bookshelf.yml`)
- [ ] **Add workflow artifacts** to save error screenshots on failures
- [ ] **Add Slack/email notifications** for workflow failures
- [ ] **Remove legacy scraper** after 2-3 months of successful runs
- [ ] **Add retry logic** for transient network errors
- [ ] **Session persistence** - Save cookies between runs to avoid repeated logins

### Long-term Considerations

- [ ] **Monitor for HTML changes** - Goodreads may update their UI
- [ ] **Rate limiting** - Watch for HTTP 429 responses
- [ ] **2FA support** - If Goodreads adds mandatory 2FA, will need to handle it
- [ ] **Alternative auth methods** - Consider OAuth if available via Goodreads API

---

## Rollback Plan

If the Playwright scraper fails and you need to revert:

1. **Update GitHub Actions workflow** to use legacy scraper:
   ```yaml
   - name: Run 00_goodreads_scraper_legacy.py
     run: python3 ${{ github.workspace }}/src/bookshelf/syncer_v2/00_goodreads_scraper_legacy.py
   ```

2. **Remove Playwright browser installation step**

3. **Note**: Legacy scraper will fail on authenticated pages, only works if Goodreads removes auth requirement

**Better approach**: Fix the Playwright scraper rather than reverting, since the underlying issue (auth requirement) won't go away.

---

## Architecture Decisions

### Why Playwright vs Selenium?

- **Playwright**: Modern, faster, better headless support, built-in waiting
- **Selenium**: Older, more dependencies, requires separate WebDriver

### Why Fail on CAPTCHA vs Handle It?

- CAPTCHAs require human intervention anyway
- Clear failure is better than silent degradation
- Allows admin to take corrective action

### Why Reuse Parsing Logic?

- Proven to work over time
- Reduces migration risk
- Maintains output format compatibility
- Easier to debug if issues arise

### Why Keep Legacy Scraper?

- Safety net for emergency rollback
- Reference for parsing logic
- Documentation of original implementation
- Can be removed after confidence is established

---

## Support

For issues or questions:

1. Check error screenshots in `src/bookshelf/syncer_v2/error_*.png`
2. Review GitHub Actions workflow logs
3. Verify credentials are correct
4. Test locally to isolate GitHub Actions vs code issues
5. Check if Goodreads made UI changes (compare with `00_goodreads_scraper_legacy.py` assumptions)

---

## Appendix: File Locations

```
src/bookshelf/syncer_v2/
├── 00_goodreads_scraper_playwright.py  # NEW: Main scraper with Playwright
├── 00_goodreads_scraper_legacy.py      # RENAMED: Old requests-based scraper
├── 02_all_books_flattener.py           # Unchanged
├── 03_show_missing_thumbnails.py       # Unchanged
├── requirements.txt                     # Modified: Added playwright, python-dotenv
├── .env.example                         # NEW: Credential template
├── .env                                 # NOT IN REPO: Your local credentials
├── all_books.json                       # Output (same format as before)
├── all_books_flattened.json            # Output (same format as before)
├── HANDOFF.md                          # This file
└── error_*.png                         # Error screenshots (generated on failure)
```

```
.github/workflows/
└── sync_bookshelf.yml                  # Modified: Updated for Playwright
```

```
.gitignore                              # Modified: Added credential files
```

---

**End of Handoff Document**

*Last Updated: January 27, 2026*
