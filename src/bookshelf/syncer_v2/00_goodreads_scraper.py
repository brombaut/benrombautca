from time import sleep
import xml.etree.ElementTree as ET
import email.utils
import json
import logging
import os
import re
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

USER_ID = "115130270"
RSS_BASE = "https://www.goodreads.com/review/list_rss/{user_id}?shelf={shelf}&page={page}"


class Bookshelf:
    TO_READ = "toread_books"
    READ = "read_books"
    CURRENTLY_READING = "currentlyreading_books"


def dict_to_json_file(data, file_path):
    logger.debug(f"[dict_to_json_file] Writing data to {file_path}")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    logger.debug(f"[dict_to_json_file] Data written to {file_path}")


def fetch_shelf(shelf):
    """Fetch all items from a shelf by paginating through the RSS feed."""
    logger.debug(f"[fetch_shelf] Fetching shelf: {shelf}")
    items = []
    page = 1
    while True:
        url = RSS_BASE.format(user_id=USER_ID, shelf=shelf, page=page)
        logger.debug(f"[fetch_shelf] Fetching page {page}: {url}")
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        channel = root.find("channel")
        page_items = channel.findall("item") if channel is not None else []
        if not page_items:
            break
        items.extend(page_items)
        page += 1
        sleep(1)
    logger.debug(f"[fetch_shelf] Fetched {len(items)} items from shelf: {shelf}")
    return items


def text(item, tag):
    """Extract text content of a child element, returning empty string if absent."""
    el = item.find(tag)
    return (el.text or "").strip() if el is not None else ""


def parse_book_id_slug(item):
    """Extract the full book slug from the <description> HTML link.

    The description contains an href like:
      https://www.goodreads.com/book/show/271285.Into_Thin_Air?utm_medium=...
    We want just the slug (e.g. '271285.Into_Thin_Air') which matches the
    thumbnail filename on disk. Falls back to the numeric <book_id> if not found.
    """
    desc = text(item, "description")
    m = re.search(r'goodreads\.com/book/show/([^"\s?]+)', desc)
    if m:
        return m.group(1)
    return text(item, "book_id")


def parse_link(item):
    """Extract the review URL from an RSS <item>. In RSS 2.0, <link> is a text node;
    ElementTree may return its content as the tail of the preceding sibling element."""
    # Try direct child tag first
    el = item.find("link")
    if el is not None and (el.text or "").strip():
        return el.text.strip()
    # Fallback: ElementTree sometimes stores <link> text as tail of the preceding sibling
    children = list(item)
    for i, child in enumerate(children):
        if child.tag == "link" and i > 0:
            tail = (children[i - 1].tail or "").strip()
            if tail:
                return tail
    return ""


def parse_num_pages(item):
    """Extract num_pages from the <book num_pages="..."> attribute."""
    book_el = item.find("book")
    if book_el is not None:
        val = book_el.get("num_pages") or (book_el.text or "").strip()
        try:
            return int(val)
        except (TypeError, ValueError):
            pass
    return None


def normalize_date(date_str):
    """Parse RFC 2822 date string to YYYY-MM-DD. Returns None if empty or unparseable."""
    if not date_str:
        return None
    try:
        parsed = email.utils.parsedate(date_str)
        if parsed is None:
            return None
        dt = email.utils.parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


def parse_read_books(items):
    logger.debug(f"[parse_read_books] Parsing {len(items)} read books")
    books = []
    for item in items:
        book = {
            "title": text(item, "title"),
            "author": text(item, "author_name"),
            "book_id": parse_book_id_slug(item),
            "link": parse_link(item),
            "date_finished": normalize_date(text(item, "user_read_at")),
            "rating": int(text(item, "user_rating") or 0),
            "avg_rating": float(text(item, "average_rating") or 0),
            "isbn": text(item, "isbn") or None,
            "review": text(item, "user_review") or None,
            "numPages": parse_num_pages(item),
        }
        books.append(book)
    logger.debug(f"[parse_read_books] Parsed {len(books)} read books")
    return books


def parse_toread_books(items):
    logger.debug(f"[parse_toread_books] Parsing {len(items)} to-read books")
    # RSS returns newest-first; reverse so position 1 = first added
    items_oldest_first = list(reversed(items))
    books = []
    for i, item in enumerate(items_oldest_first, start=1):
        book = {
            "title": text(item, "title"),
            "author": text(item, "author_name"),
            "book_id": parse_book_id_slug(item),
            "link": parse_link(item),
            "date_added": normalize_date(text(item, "user_date_added")),
            "position": i,
            "avg_rating": float(text(item, "average_rating") or 0),
            "numPages": parse_num_pages(item),
        }
        books.append(book)
    logger.debug(f"[parse_toread_books] Parsed {len(books)} to-read books")
    return books


def parse_currentlyreading_books(items):
    logger.debug(f"[parse_currentlyreading_books] Parsing {len(items)} currently-reading books")
    books = []
    for item in items:
        book = {
            "title": text(item, "title"),
            "author": text(item, "author_name"),
            "book_id": parse_book_id_slug(item),
            "link": parse_link(item),
            "date_added": normalize_date(text(item, "user_date_added")),
            "avg_rating": float(text(item, "average_rating") or 0),
            "numPages": parse_num_pages(item),
        }
        books.append(book)
    logger.debug(f"[parse_currentlyreading_books] Parsed {len(books)} currently-reading books")
    return books


def main():
    logger.debug("[main] Starting main function")
    read_items = fetch_shelf("read")
    toread_items = fetch_shelf("to-read")
    currentlyreading_items = fetch_shelf("currently-reading")

    read_books = parse_read_books(read_items)
    toread_books = parse_toread_books(toread_items)
    currentlyreading_books = parse_currentlyreading_books(currentlyreading_items)

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
