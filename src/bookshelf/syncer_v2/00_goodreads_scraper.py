import re
from time import sleep
import requests
from bs4 import BeautifulSoup

class Bookshelf:
    TO_READ = "toread_books"
    READ = "read_books"
    CURRENTLY_READING = "currentlyreading_books"

def dict_to_json_file(data, file_path):
    import json
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Error get_html status_code={response.status_code} response.text={response.text}")

def get_profile_html():
    html = get_html("https://www.goodreads.com/user/show/115130270-ben-rombaut")
    return html


def get_book_title_from_html_row(tr_html):
    title_td = tr_html.find('td', {'class': 'field title'})
    title = title_td.find('a').text.strip()
    title = title.split("\n")[0]
    title = title.replace('\u2019', "'")
    return title

def get_book_author_from_html_row(tr_html):
    author_td = tr_html.find('td', {'class': 'field author'})
    author = author_td.find('a').text.strip()
    # Will turn "Lastname, Firstname" into "Firstname Lastname"
    author = author.split(",")[1].strip() + " " + author.split(",")[0].strip()
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
    return lookup_table[rating_text]

def get_book_date_read_from_html_row(tr_html):
    date_read_td = tr_html.find('td', {'class': 'field date_read'})
    date_read = date_read_td.find('div').text.strip()
    return date_read

def get_book_date_added_from_html_row(tr_html):
    date_read_td = tr_html.find('td', {'class': 'field date_added'})
    date_read = date_read_td.find('div').text.strip()
    return date_read

def get_book_id_from_html_row(tr_html):
    book_id_td = tr_html.find('td', {'class': 'field title'})
    book_id = book_id_td.find('a')['href'].split('/')[-1]
    return book_id
    # number_part = re.match(r'^\d+', book_url).group()
    # return int(number_part)

def get_book_review_id_from_html_row(tr_html):
    actions_td = tr_html.find('td', {'class': 'field actions'})
    actions_link_url = actions_td.find('a')['href']
    review_id = actions_link_url.split('/')[-1]
    return int(review_id)

def get_book_review_link_from_html_row(tr_html):
    actions_td = tr_html.find('td', {'class': 'field actions'})
    actions_link_url = actions_td.find('a')['href']
    review_link = f"https://www.goodreads.com{actions_link_url}"
    return review_link

def get_book_position_from_html_row(tr_html):
    position_td = tr_html.find('td', {'class': 'field position'})
    position = position_td.find('div').text.strip()
    return int(position)

def parse_read_books_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    books = []
    for tr in soup.find_all('tr', {'class': 'bookalike review'}):
        book = {
            'title': get_book_title_from_html_row(tr),
            'author': get_book_author_from_html_row(tr),
            "book_id": get_book_id_from_html_row(tr),
            "review_id": get_book_review_id_from_html_row(tr),
            'date_finished': get_book_date_read_from_html_row(tr),
            'rating': get_book_rating_from_html_row(tr),
        }
        books.append(book)
    return books

def parse_toread_books_from_html(html):
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
    return books

# def parse_currentlyreading_books_from_html(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     books = []
#     for tr in soup.find_all('tr', {'class': 'bookalike review'}):
#         book = {
#             'title': get_book_title_from_html_row(tr),
#             'author': get_book_author_from_html_row(tr),
#             'book_id': get_book_id_from_html_row(tr),
#             'review_id': get_book_review_id_from_html_row(tr),
#             "date_added": get_book_date_added_from_html_row(tr),
#             "review_link": get_book_review_link_from_html_row(tr),
#         }
#         books.append(book)
#     return books

def get_books_for_shelf(shelf, parsing_fn, debug=False):
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
    return books

def get_currently_reading_books():
    def format_date_string(date_string):
        # Format is "Oct 23, 2024 05:56PM", "want Oct 23, 2024"
        return date_string.split(" ")[0] + " " + date_string.split(" ")[1] + " " + date_string.split(" ")[2]
    def parse_on_page_from_review_div(review_div):
        link_to_progress_text = review_div.find('a', {'class': 'greyText smallText'}).text.strip()
        # format is "(page 100 of 200)", get the first number
        return int(link_to_progress_text.split(" ")[1])
    def parse_num_pages_from_review_div(review_div):
        link_to_progress_text = review_div.find('a', {'class': 'greyText smallText'}).text.strip()
        # format is "(page 100 of 200)", get the last number
        return int(link_to_progress_text.split(" ")[3][:-1])
    profile_html = get_html("https://www.goodreads.com/user/show/115130270-ben-rombaut")
    soup = BeautifulSoup(profile_html, 'html.parser')
    currently_reading_books = []
    currently_reading_reviews_html = soup.find('div', {'id': 'currentlyReadingReviews'})
    for review_div in currently_reading_reviews_html.find_all('div', {'class': 'Updates'}):
        book = {
            'title': review_div.find('a', {'class': 'bookTitle'}).text.strip(),
            'author': review_div.find('a', {'class': 'authorName'}).text.strip(),
            'book_id': review_div.find('a', {'class': 'bookTitle'})['href'].split('/')[-1],
            'review_id': int(review_div.find('a', {'class': 'updatedTimestamp'})['href'].split('/')[-1]),
            "date_added": format_date_string(review_div.find('a', {'class': 'updatedTimestamp'}).text.strip()),
            "onPage": parse_on_page_from_review_div(review_div),
            "numPages": parse_num_pages_from_review_div(review_div),
        }
        currently_reading_books.append(book)
    return currently_reading_books


def main():
    debug=False
    read_books = get_books_for_shelf("read", parse_read_books_from_html, debug=debug)
    toread_books = get_books_for_shelf("to-read", parse_toread_books_from_html, debug=debug)
    # currentlyreading_books = get_books_for_shelf("currently-reading", parse_currentlyreading_books_from_html)
    currentlyreading_books = get_currently_reading_books()
    all_books = {
        Bookshelf.TO_READ: toread_books,
        Bookshelf.CURRENTLY_READING: currentlyreading_books,
        Bookshelf.READ: read_books,
    }
    dict_to_json_file(all_books, 'all_books.json')
    # print(read_books)

if __name__ == "__main__":
    main()