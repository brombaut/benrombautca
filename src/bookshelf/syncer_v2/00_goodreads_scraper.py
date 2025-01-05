from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import logging
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Construct the path for the log file
# log_file_path = os.path.join(script_dir, "00_goodreads_scraper.log")
# file_handler = logging.FileHandler(log_file_path, mode='w')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

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

def get_html(url):
    logger.debug(f"[get_html] Fetching HTML for URL: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logger.debug(f"[get_html] Successfully fetched HTML for URL: {url}")
        return response.text
    logger.error(f"[get_html] Error fetching HTML for URL: {url}, status_code={response.status_code}")
    raise Exception(f"Error get_html status_code={response.status_code} response.text={response.text}")

def get_profile_html():
    logger.debug("[get_profile_html] Fetching profile HTML")
    html = get_html("https://www.goodreads.com/user/show/115130270-ben-rombaut")
    logger.debug("[get_profile_html] Profile HTML fetched")
    return html

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

def get_book_review_link_from_html_row(tr_html):
    actions_td = tr_html.find('td', {'class': 'field actions'})
    actions_link_url = actions_td.find('a')['href']
    review_link = f"https://www.goodreads.com{actions_link_url}"
    logger.debug(f"[get_book_review_link_from_html_row] Extracted review link: {review_link}")
    return review_link

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

def get_books_for_shelf(shelf, parsing_fn, debug=False):
    logger.debug(f"[get_books_for_shelf] Fetching books for shelf: {shelf}")
    page_index = 1
    books = []
    while True:
        html = get_html(f"https://www.goodreads.com/review/list/115130270-ben-rombaut?shelf={shelf}&view=table&page={page_index}")
        books_page = parsing_fn(html)
        if len(books_page) == 0:
            break
        books += books_page
        page_index += 1
        if debug:
            break
        sleep(1)
    logger.debug(f"[get_books_for_shelf] Fetched {len(books)} books for shelf: {shelf}")
    return books

def get_currently_reading_books():
    logger.debug("[get_currently_reading_books] Fetching currently reading books")
    def parse_title_from_review_div(review_div):
        logger.debug("[parse_title_from_review_div] Parsing title from review div")
        title = review_div.find('a', {'class': 'bookTitle'}).text.strip()
        logger.debug(f"[parse_title_from_review_div] Extracted title: {title}")
        return title
    def parse_author_from_review_div(review_div):
        logger.debug("[parse_author_from_review_div] Parsing author from review div")
        author = review_div.find('a', {'class': 'authorName'}).text.strip()
        logger.debug(f"[parse_author_from_review_div] Extracted author: {author}")
        return author
    def parse_book_id_from_review_div(review_div):
        logger.debug("[parse_book_id_from_review_div] Parsing book ID from review div")
        book_id = review_div.find('a', {'class': 'bookTitle'})['href'].split('/')[-1]
        logger.debug(f"[parse_book_id_from_review_div] Extracted book ID: {book_id}")
        return book_id
    def parse_review_id_from_review_div(review_div):
        logger.debug("[parse_review_id_from_review_div] Parsing review ID from review div")
        review_id = int(review_div.find('a', {'class': 'updatedTimestamp'})['href'].split('/')[-1])
        logger.debug(f"[parse_review_id_from_review_div] Extracted review ID: {review_id}")
        return review_id
    def parse_date_added_from_review_div(review_div):
        logger.debug("[parse_date_added_from_review_div] Parsing date added from review div")
        date_added = review_div.find('a', {'class': 'updatedTimestamp'}).text.strip()
        logger.debug(f"[parse_date_added_from_review_div] Extracted date added: {date_added}")
        return date_added
    def format_date_string(date_string):
        logger.debug(f"[format_date_string] Formatting date string: {date_string}")
        formatted_date = date_string.split(" ")[0] + " " + date_string.split(" ")[1] + " " + date_string.split(" ")[2]
        logger.debug(f"[format_date_string] Formatted date string: {formatted_date}")
        return formatted_date
    def parse_on_page_from_review_div(review_div):
        try:
            logger.debug("[parse_on_page_from_review_div] Parsing on page from review div")
            link_to_progress_text = review_div.find('a', {'class': 'greyText smallText'}).text.strip()
            on_page = int(link_to_progress_text.split(" ")[1])
            logger.debug(f"[parse_on_page_from_review_div] Extracted on page: {on_page}")
            return on_page
        except Exception as e:
            logger.error(f"[parse_on_page_from_review_div] Error parsing on page: {e}. Returning 0.")
            return 0
    def parse_num_pages_from_review_div(review_div):
        try:
            logger.debug("[parse_num_pages_from_review_div] Parsing number of pages from review div")
            link_to_progress_text = review_div.find('a', {'class': 'greyText smallText'}).text.strip()
            num_pages = int(link_to_progress_text.split(" ")[3][:-1])
            logger.debug(f"[parse_num_pages_from_review_div] Extracted number of pages: {num_pages}")
            return num_pages
        except Exception as e:
            logger.error(f"[parse_num_pages_from_review_div] Error parsing number of pages: {e}. Returning 0.")
            return 0
    profile_html = get_html("https://www.goodreads.com/user/show/115130270-ben-rombaut")
    soup = BeautifulSoup(profile_html, 'html.parser')
    currently_reading_books = []
    currently_reading_reviews_html = soup.find('div', {'id': 'currentlyReadingReviews'})
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
    logger.debug(f"[get_currently_reading_books] Fetched {len(currently_reading_books)} currently reading books")
    return currently_reading_books

def main():
    logger.debug("[main] Starting main function")
    debug=False
    read_books = get_books_for_shelf("read", parse_read_books_from_html, debug=debug)
    toread_books = get_books_for_shelf("to-read", parse_toread_books_from_html, debug=debug)
    currentlyreading_books = get_currently_reading_books()
    all_books = {
        Bookshelf.TO_READ: toread_books,
        Bookshelf.CURRENTLY_READING: currentlyreading_books,
        Bookshelf.READ: read_books,
    }
    all_books_json_file_path = os.path.join(script_dir, "all_books.json")
    dict_to_json_file(all_books, all_books_json_file_path)
    logger.debug("[main] Main function completed")

if __name__ == "__main__":
    main()