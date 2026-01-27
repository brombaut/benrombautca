from time import sleep
from bs4 import BeautifulSoup
import json
import logging
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Load environment variables
load_dotenv()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class Bookshelf:
    TO_READ = "toread_books"
    READ = "read_books"
    CURRENTLY_READING = "currentlyreading_books"


def dict_to_json_file(data, file_path):
    logger.debug(f"[dict_to_json_file] Writing data to {file_path}")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    logger.debug(f"[dict_to_json_file] Data written to {file_path}")


# Reused parsing functions from legacy scraper
def get_book_title_from_html_row(tr_html):
    title_td = tr_html.find('td', {'class': 'field title'})
    title = title_td.find('a').text.strip()
    title = title.split("\n")[0]
    title = title.replace('\u2019', "'")
    logger.debug(f"[get_book_title_from_html_row] Extracted title: {title}")
    return title


def get_book_author_from_html_row(tr_html):
    author_td = tr_html.find('td', {'class': 'field author'})
    author = author_td.find('a').text.strip()
    author = author.split(",")[1].strip() + " " + author.split(",")[0].strip()
    logger.debug(f"[get_book_author_from_html_row] Extracted author: {author}")
    return author


def get_book_rating_from_html_row(tr_html):
    rating_td = tr_html.find('td', {'class': 'field rating'})
    rating_text = rating_td.find('span').text.strip()
    lookup_table = {
        "": 0,
        "did not like it": 1,
        "it was ok": 2,
        "liked it": 3,
        "really liked it": 4,
        "it was amazing": 5
    }
    result = lookup_table.get(rating_text)
    if result is None:
        logger.error(f"[get_book_rating_from_html_row] Rating text not found: {rating_text}")
    logger.debug(f"[get_book_rating_from_html_row] Extracted rating: {result}")
    return result


def get_book_dates_read_from_html_row(tr_html):
    date_read_td = tr_html.find('td', {'class': 'field date_read'})
    date_row_divs = date_read_td.find_all('div', {'class': 'date_row'})
    dates_read = list()
    for date_row_div in date_row_divs:
        dates_read.append(date_row_div.text.strip())
    logger.debug(f"[get_book_dates_read_from_html_row] Extracted dates read: {dates_read}")
    return dates_read


def get_book_date_added_from_html_row(tr_html):
    date_read_td = tr_html.find('td', {'class': 'field date_added'})
    date_read = date_read_td.find('div').text.strip()
    logger.debug(f"[get_book_date_added_from_html_row] Extracted date added: {date_read}")
    return date_read


def get_book_id_from_html_row(tr_html):
    book_id_td = tr_html.find('td', {'class': 'field title'})
    book_id = book_id_td.find('a')['href'].split('/')[-1]
    logger.debug(f"[get_book_id_from_html_row] Extracted book ID: {book_id}")
    return book_id


def get_book_review_id_from_html_row(tr_html):
    actions_td = tr_html.find('td', {'class': 'field actions'})
    actions_link_url = actions_td.find('a')['href']
    review_id = actions_link_url.split('/')[-1]
    logger.debug(f"[get_book_review_id_from_html_row] Extracted review ID: {review_id}")
    return int(review_id)


def get_book_position_from_html_row(tr_html):
    position_td = tr_html.find('td', {'class': 'field position'})
    position = position_td.find('div').text.strip()
    logger.debug(f"[get_book_position_from_html_row] Extracted position: {position}")
    return int(position)


def parse_read_books_from_html(html):
    logger.debug("[parse_read_books_from_html] Parsing read books from HTML")
    soup = BeautifulSoup(html, 'html.parser')
    books = []
    for tr in soup.find_all('tr', {'class': 'bookalike review'}):
        dates_read = get_book_dates_read_from_html_row(tr)
        if len(dates_read) > 1:
            logger.debug(f"[parse_read_books_from_html] Book with multiple dates read: {get_book_title_from_html_row(tr)}")
        duplicate_review_id = None
        for date_read in dates_read:
            final_review_id = str(get_book_review_id_from_html_row(tr))
            review_id = final_review_id if not duplicate_review_id else f"{final_review_id}.{duplicate_review_id}"
            book = {
                'title': get_book_title_from_html_row(tr),
                'author': get_book_author_from_html_row(tr),
                "book_id": get_book_id_from_html_row(tr),
                "review_id": review_id,
                'date_finished': date_read,
                'rating': get_book_rating_from_html_row(tr),
            }
            books.append(book)
            duplicate_review_id = duplicate_review_id + 1 if duplicate_review_id else 1
    logger.debug(f"[parse_read_books_from_html] Parsed {len(books)} read books")
    return books


def parse_toread_books_from_html(html):
    logger.debug("[parse_toread_books_from_html] Parsing to-read books from HTML")
    soup = BeautifulSoup(html, 'html.parser')
    books = []
    for tr in soup.find_all('tr', {'class': 'bookalike review'}):
        book = {
            'title': get_book_title_from_html_row(tr),
            'author': get_book_author_from_html_row(tr),
            'book_id': get_book_id_from_html_row(tr),
            'review_id': get_book_review_id_from_html_row(tr),
            "date_added": get_book_date_added_from_html_row(tr),
            "position": get_book_position_from_html_row(tr),
        }
        books.append(book)
    logger.debug(f"[parse_toread_books_from_html] Parsed {len(books)} to-read books")
    return books


def parse_currently_reading_from_profile_html(html):
    logger.debug("[parse_currently_reading_from_profile_html] Parsing currently reading books")

    def parse_title_from_review_div(review_div):
        title = review_div.find('a', {'class': 'bookTitle'}).text.strip()
        logger.debug(f"[parse_title_from_review_div] Extracted title: {title}")
        return title

    def parse_author_from_review_div(review_div):
        author = review_div.find('a', {'class': 'authorName'}).text.strip()
        logger.debug(f"[parse_author_from_review_div] Extracted author: {author}")
        return author

    def parse_book_id_from_review_div(review_div):
        book_id = review_div.find('a', {'class': 'bookTitle'})['href'].split('/')[-1]
        logger.debug(f"[parse_book_id_from_review_div] Extracted book ID: {book_id}")
        return book_id

    def parse_review_id_from_review_div(review_div):
        review_id = int(review_div.find('a', {'class': 'updatedTimestamp'})['href'].split('/')[-1])
        logger.debug(f"[parse_review_id_from_review_div] Extracted review ID: {review_id}")
        return review_id

    def parse_date_added_from_review_div(review_div):
        date_added = review_div.find('a', {'class': 'updatedTimestamp'}).text.strip()
        logger.debug(f"[parse_date_added_from_review_div] Extracted date added: {date_added}")
        return date_added

    def format_date_string(date_string):
        formatted_date = date_string.split(" ")[0] + " " + date_string.split(" ")[1] + " " + date_string.split(" ")[2]
        logger.debug(f"[format_date_string] Formatted date string: {formatted_date}")
        return formatted_date

    def parse_on_page_from_review_div(review_div):
        try:
            link_to_progress_text = review_div.find('a', {'class': 'greyText smallText'}).text.strip()
            on_page = int(link_to_progress_text.split(" ")[1])
            logger.debug(f"[parse_on_page_from_review_div] Extracted on page: {on_page}")
            return on_page
        except Exception as e:
            logger.error(f"[parse_on_page_from_review_div] Error parsing on page: {e}. Returning 0.")
            return 0

    def parse_num_pages_from_review_div(review_div):
        try:
            link_to_progress_text = review_div.find('a', {'class': 'greyText smallText'}).text.strip()
            num_pages = int(link_to_progress_text.split(" ")[3][:-1])
            logger.debug(f"[parse_num_pages_from_review_div] Extracted number of pages: {num_pages}")
            return num_pages
        except Exception as e:
            logger.error(f"[parse_num_pages_from_review_div] Error parsing number of pages: {e}. Returning 0.")
            return 0

    soup = BeautifulSoup(html, 'html.parser')
    currently_reading_books = []
    currently_reading_reviews_html = soup.find('div', {'id': 'currentlyReadingReviews'})
    if currently_reading_reviews_html is None:
        logger.warning("[parse_currently_reading_from_profile_html] No currently reading reviews found")
        return []
    for review_div in currently_reading_reviews_html.find_all('div', {'class': 'Updates'}):
        book = {
            'title': parse_title_from_review_div(review_div),
            'author': parse_author_from_review_div(review_div),
            'book_id': parse_book_id_from_review_div(review_div),
            'review_id': parse_review_id_from_review_div(review_div),
            "date_added": format_date_string(parse_date_added_from_review_div(review_div)),
            "onPage": parse_on_page_from_review_div(review_div),
            "numPages": parse_num_pages_from_review_div(review_div),
        }
        currently_reading_books.append(book)
    logger.debug(f"[parse_currently_reading_from_profile_html] Fetched {len(currently_reading_books)} currently reading books")
    return currently_reading_books


def authenticate_goodreads(page, email, password):
    """Authenticate to Goodreads using email/password through Amazon auth portal."""
    logger.info("[authenticate_goodreads] Starting authentication process")

    try:
        # Navigate to sign-in page
        logger.debug("[authenticate_goodreads] Navigating to sign-in page")
        page.goto("https://www.goodreads.com/user/sign_in", wait_until="networkidle")

        # Check for CAPTCHA
        page_content = page.content()
        if "captcha" in page_content.lower() or "security check" in page_content.lower():
            logger.error("[authenticate_goodreads] CAPTCHA detected on sign-in page")
            page.screenshot(path=os.path.join(script_dir, "error_captcha.png"))
            raise Exception("CAPTCHA detected - manual intervention required")

        # Click "Sign in with email" button
        logger.debug("[authenticate_goodreads] Clicking 'Sign in with email' button")
        page.click("button.authPortalSignInButton, a:has(button.authPortalSignInButton)", timeout=10000)
        page.wait_for_load_state("networkidle")

        # Wait for Amazon auth portal to load
        logger.debug("[authenticate_goodreads] Waiting for Amazon auth portal")
        page.wait_for_url("**/ap/signin**", timeout=15000)

        # Check for CAPTCHA on Amazon portal
        page_content = page.content()
        if "captcha" in page_content.lower() or "enter the characters" in page_content.lower():
            logger.error("[authenticate_goodreads] CAPTCHA detected on Amazon auth portal")
            page.screenshot(path=os.path.join(script_dir, "error_captcha_amazon.png"))
            raise Exception("CAPTCHA detected on Amazon auth portal - manual intervention required")

        # Enter email
        logger.debug("[authenticate_goodreads] Entering email")
        page.fill("input[type='email'], input[name='email']", email)

        # Enter password
        logger.debug("[authenticate_goodreads] Entering password")
        page.fill("input[type='password'], input[name='password']", password)

        # Click sign-in button
        logger.debug("[authenticate_goodreads] Clicking sign-in button")
        page.click("input[type='submit'], button[type='submit']")

        # Wait for redirect back to Goodreads
        logger.debug("[authenticate_goodreads] Waiting for redirect to Goodreads")
        page.wait_for_url("**/goodreads.com/**", timeout=20000)

        # Verify authentication by checking for user-specific elements
        logger.debug("[authenticate_goodreads] Verifying authentication")
        page_content = page.content()

        # Check if still on sign-in page (authentication failed)
        if "sign in to goodreads" in page_content.lower() or "sign in with email" in page_content.lower():
            logger.error("[authenticate_goodreads] Authentication failed - still on sign-in page")
            page.screenshot(path=os.path.join(script_dir, "error_auth_failed.png"))
            raise Exception("Authentication failed - verify credentials are correct")

        logger.info("[authenticate_goodreads] Authentication successful!")
        return True

    except PlaywrightTimeoutError as e:
        logger.error(f"[authenticate_goodreads] Timeout during authentication: {e}")
        page.screenshot(path=os.path.join(script_dir, "error_timeout.png"))
        raise Exception(f"Authentication timeout: {e}")
    except Exception as e:
        logger.error(f"[authenticate_goodreads] Authentication error: {e}")
        page.screenshot(path=os.path.join(script_dir, "error_auth.png"))
        raise


def get_shelf_html_authenticated(page, user_id, shelf, page_num):
    """Navigate to a shelf page and return the HTML."""
    url = f"https://www.goodreads.com/review/list/{user_id}?shelf={shelf}&view=table&page={page_num}"
    logger.debug(f"[get_shelf_html_authenticated] Navigating to: {url}")

    try:
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Check if we got redirected to sign-in (session expired)
        if "sign in" in page.url.lower():
            logger.error("[get_shelf_html_authenticated] Redirected to sign-in page - session expired")
            raise Exception("Session expired - re-authentication needed")

        html = page.content()
        logger.debug(f"[get_shelf_html_authenticated] Retrieved HTML ({len(html)} chars)")
        return html

    except PlaywrightTimeoutError as e:
        logger.error(f"[get_shelf_html_authenticated] Timeout loading shelf page: {e}")
        page.screenshot(path=os.path.join(script_dir, f"error_shelf_{shelf}_page{page_num}.png"))
        raise Exception(f"Timeout loading shelf page: {e}")


def get_books_for_shelf_authenticated(page, user_id, shelf, parsing_fn, debug=False):
    """Scrape all books from a shelf with pagination."""
    logger.debug(f"[get_books_for_shelf_authenticated] Fetching books for shelf: {shelf}")
    page_index = 1
    books = []

    while True:
        html = get_shelf_html_authenticated(page, user_id, shelf, page_index)
        books_page = parsing_fn(html)

        if len(books_page) == 0:
            logger.debug(f"[get_books_for_shelf_authenticated] No more books found on page {page_index}")
            break

        books += books_page
        logger.debug(f"[get_books_for_shelf_authenticated] Fetched {len(books_page)} books from page {page_index}")
        page_index += 1

        if debug:
            logger.debug("[get_books_for_shelf_authenticated] Debug mode - stopping after first page")
            break

        sleep(1)  # Rate limiting

    logger.debug(f"[get_books_for_shelf_authenticated] Fetched {len(books)} total books for shelf: {shelf}")
    return books


def main():
    logger.info("[main] Starting Goodreads scraper with Playwright")

    # Load credentials from environment
    email = os.getenv('GOODREADS_EMAIL')
    password = os.getenv('GOODREADS_PASSWORD')
    user_id = os.getenv('GOODREADS_USER_ID', '115130270-ben-rombaut')

    if not email or not password:
        logger.error("[main] Missing GOODREADS_EMAIL or GOODREADS_PASSWORD environment variables")
        raise Exception("Missing required environment variables: GOODREADS_EMAIL, GOODREADS_PASSWORD")

    logger.info(f"[main] Using user ID: {user_id}")

    debug = False

    with sync_playwright() as p:
        # Launch browser
        logger.info("[main] Launching browser")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        try:
            # Authenticate
            authenticate_goodreads(page, email, password)

            # Scrape read books
            logger.info("[main] Scraping read books")
            read_books = get_books_for_shelf_authenticated(page, user_id, "read", parse_read_books_from_html, debug=debug)

            # Scrape to-read books
            logger.info("[main] Scraping to-read books")
            toread_books = get_books_for_shelf_authenticated(page, user_id, "to-read", parse_toread_books_from_html, debug=debug)

            # Scrape currently reading books from profile
            logger.info("[main] Scraping currently reading books")
            page.goto(f"https://www.goodreads.com/user/show/{user_id}", wait_until="networkidle")
            profile_html = page.content()
            currentlyreading_books = parse_currently_reading_from_profile_html(profile_html)

            # Combine results
            all_books = {
                Bookshelf.TO_READ: toread_books,
                Bookshelf.CURRENTLY_READING: currentlyreading_books,
                Bookshelf.READ: read_books,
            }

            # Write to JSON file
            all_books_json_file_path = os.path.join(script_dir, "all_books.json")
            dict_to_json_file(all_books, all_books_json_file_path)

            logger.info(f"[main] Scraping completed successfully!")
            logger.info(f"[main] Total books - Read: {len(read_books)}, To-read: {len(toread_books)}, Currently reading: {len(currentlyreading_books)}")

        except Exception as e:
            logger.error(f"[main] Scraping failed: {e}")
            raise
        finally:
            browser.close()
            logger.info("[main] Browser closed")


if __name__ == "__main__":
    main()
