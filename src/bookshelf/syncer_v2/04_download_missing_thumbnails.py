"""
Download missing book thumbnails from AbeBooks search results.

For each book in all_books_flattened.json that doesn't have a .webp thumbnail,
searches AbeBooks by title + author, downloads the first cover image, and
converts it to webp.
"""

from time import sleep
from urllib.parse import quote
import io
import json
import logging
import os
import re
import requests
from PIL import Image

script_dir = os.path.dirname(os.path.abspath(__file__))
THUMBS_DIR = os.path.join(script_dir, "book_thumbnails_v2")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def find_missing_books():
    flattened_path = os.path.join(script_dir, "all_books_flattened.json")
    with open(flattened_path) as f:
        books = json.load(f)
    missing = []
    for book in books:
        thumb_path = os.path.join(THUMBS_DIR, f"{book['book_id']}.webp")
        if not os.path.exists(thumb_path):
            missing.append(book)
    return missing


def search_abebooks_cover(title, author):
    """Search AbeBooks and return the src URL of the first cover image, or None."""
    query = f"{title} {author}".strip()
    url = f"https://www.abebooks.com/servlet/SearchResults?ds=20&kn={quote(query)}&sts=t"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        m = re.search(r'class="srp-item-image"[^>]+src="([^"]+)"', resp.text)
        if m:
            return m.group(1)
    except Exception as e:
        logger.error(f"AbeBooks search failed for '{title}': {e}")
    return None


def download_and_save_webp(image_url, dest_path):
    """Download image from URL and save as webp at dest_path."""
    resp = requests.get(image_url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    img = Image.open(io.BytesIO(resp.content)).convert("RGB")
    img.save(dest_path, "webp")


def main():
    missing = find_missing_books()
    logger.info(f"Found {len(missing)} books with missing thumbnails")

    succeeded = 0
    failed = []

    for book in missing:
        title = book["title"]
        author = book["author"]
        book_id = book["book_id"]
        dest_path = os.path.join(THUMBS_DIR, f"{book_id}.webp")

        logger.info(f"Searching: {title} — {author}")
        cover_url = search_abebooks_cover(title, author)

        if not cover_url:
            logger.warning(f"  No cover found for: {title}")
            failed.append(book)
            sleep(1)
            continue

        logger.info(f"  Downloading: {cover_url}")
        try:
            download_and_save_webp(cover_url, dest_path)
            logger.info(f"  Saved: {dest_path}")
            succeeded += 1
        except Exception as e:
            logger.error(f"  Failed to download/convert: {e}")
            failed.append(book)

        sleep(1)

    logger.info(f"\nDone. {succeeded} downloaded, {len(failed)} failed.")
    if failed:
        logger.info("Failed books:")
        for b in failed:
            logger.info(f"  {b['title']} -- {b['author']}")


if __name__ == "__main__":
    main()
