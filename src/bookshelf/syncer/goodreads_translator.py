import requests
import xmltodict
import json
import os
from decouple import config
from argparse import ArgumentParser

GOODREADS_ID = config('VUE_APP_GOODREADS_ID')
GOODREADS_KEY = config('VUE_APP_GOODREADS_KEY')

parser = ArgumentParser()
parser.add_argument(
    "-wd",
    "--working-directory",
    dest="working_directory",
    default="./"
)
args = parser.parse_args()

WORKING_DIRECTORY = os.path.join(args.working_directory, '')


def run():
    response_as_xml = fetch_bookshelf()
    response_as_json = xml_to_json(response_as_xml)
    to_read_orders = get_to_read_order_from_gr()
    my_books = flatten_to_books(response_as_json, to_read_orders)
    write(my_books)


def fetch_bookshelf():
    url = f'https://www.goodreads.com/review/list?v=2&key={GOODREADS_KEY}&id={GOODREADS_ID}&per_page=199&page=1'
    response = requests.get(url)
    xml_response = response.text
    return xml_response


def xml_to_json(xml):
    data_dict = xmltodict.parse(xml)
    return data_dict


def get_to_read_order_from_gr():
    def fetch_to_read_bookshelf():
        url = f'https://www.goodreads.com/review/list?v=2&key={GOODREADS_KEY}&id={GOODREADS_ID}&per_page=199&page=1&shelf=to-read&sort=position'
        response = requests.get(url)
        xml_response = response.text
        return xml_response

    def parse_to_read_orders(to_read_shelf):
        to_read_gr_books = books(to_read_shelf)
        i = 0
        result = {}
        for gr_book_review in to_read_gr_books:
            b_isbn13 = gr_book_review['book']['isbn13']
            if type(b_isbn13) == str:
                result[b_isbn13] = i
            i += 1
        return result

    response_as_xml = fetch_to_read_bookshelf()
    response_as_json = xml_to_json(response_as_xml)
    return parse_to_read_orders(response_as_json)


def flatten_to_books(gr_response, to_read_orders):
    gr_books = books(gr_response)
    return simplify(gr_books, to_read_orders)


def books(gr_response):
    return gr_response['GoodreadsResponse']['reviews']['review']


def simplify(gr_books, to_read_orders):
    result = list()
    for b in gr_books:
        authors = list()
        if len(b['book']['authors']) > 1:
            print(b['book']['authors'])
        for key, a in b['book']['authors'].items():
            authors.append(a['name'])
        b_isbn13 = b['book']['isbn13']
        if not type(b_isbn13) == str:
            b_isbn13 = ''
        parsed_book = {
            'title': b['book']['title'],
            'short_title': b['book']['title_without_series'],
            'authors': ' & '.join(authors),
            'isbn13': b_isbn13,
            'link': b['book']['link'],
            'num_pages': b['book']['num_pages'],
            'dateStarted': b['started_at'],
            'dateFinished': b['read_at'],
            'rating': b['rating'],
            'shelf': b['shelves']['shelf']['@name'],
            'goodreads_review_id': b['id'],
        }
        parsed_book = add_on_page(parsed_book)
        parsed_book = add_to_read_order(parsed_book, to_read_orders)
        result.append(parsed_book)
    return result


def add_on_page(book):
    def get_on_page_from_gr(review_id):
        try:
            response_as_xml = fetch_review(review_id)
            response_as_json = xml_to_json(response_as_xml)
            on_page = parse_current_on_page(response_as_json)
            return on_page
        except Exception as e:
            print(f"Error get_on_page_from_gr: {e}")
            return 0

    def fetch_review(review_id):
        url = f'https://www.goodreads.com/review/show?v=2&key={GOODREADS_KEY}&id={review_id}&per_page=199&page=1'
        response = requests.get(url)
        xml_response = response.text
        return xml_response

    def parse_current_on_page(review_json):
        on_page = 0
        user_review = review_json['GoodreadsResponse']['review']
        if "user_statuses" not in user_review:
            return on_page
        user_statuses = user_review['user_statuses']['user_status']
        # Multiple user status updates
        if type(user_statuses) == list:
            for s in user_statuses:
                try:
                    on_page = parse_page_int_from_status(s, on_page)
                except Exception:
                    continue
        # Only 1 user status update
        else:
            try:
                on_page = parse_page_int_from_status(user_statuses, on_page)
            except Exception:
                pass
        return on_page

    def parse_page_int_from_status(status, curr_on_page):
        has_page = 'page' in status and '@type' in status['page'] and '#text' in status['page'] and status['page'][
            '@type'] == 'integer'
        if has_page:
            i_page = int(status['page']['#text'])
            if i_page > curr_on_page:
                curr_on_page = i_page
        return curr_on_page

    if book['shelf'] == 'read':
        book['on_page'] = book['num_pages']
    elif book['shelf'] == 'to-read':
        book['on_page'] = 0
    else:
        book['on_page'] = get_on_page_from_gr(book['goodreads_review_id'])
    return book


def add_to_read_order(book, to_read_orders):
    def get_to_read_order(isbn13):
        # Return 99 if we do not have the correct isbn13.
        # We can check in the f3_syncer if the firestore record has an actual int, in which case
        # we won't overwrite it with this 99. If this is a new book, the f3 record will just het
        # this value of 99
        return to_read_orders[isbn13] if isbn13 in to_read_orders else 99

    if book['shelf'] == 'to-read':
        book['to_read_order'] = get_to_read_order(book['isbn13'])
    else:
        book['to_read_order'] = None
    return book


def write(my_books):
    with open(f"{WORKING_DIRECTORY}translated_books_from_gr.json", "w") as json_file:
        json_file.write(json.dumps(my_books))


if __name__ == "__main__":
    run()
