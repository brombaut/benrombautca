import subprocess
import requests
import json
from bs4 import BeautifulSoup


class Bookshelf:
    TO_READ = "toread_books"
    READ = "read_books"
    CURRENTLY_READING = "currentlyreading_books"


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

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

##### START GET READ BOOKS #####

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

def get_book_date_added_from_html_row(tr_html):
    date_read_td = tr_html.find('td', {'class': 'field date_added'})
    date_read = date_read_td.find('div').text.strip()
    return date_read

def get_book_position_from_html_row(tr_html):
    position_td = tr_html.find('td', {'class': 'field position'})
    position = position_td.find('div').text.strip()
    return int(position)

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
        # sleep(1)
    return books

##### END GET READ BOOKS #####

##### START GET CURRENTLY_READING BOOKS #####

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

##### END GET CURRENTLY_READING BOOKS #####

def get_toread_and_currentlyreading_books_from_goodreads():
    toread_books = get_books_for_shelf("to-read", parse_toread_books_from_html, debug=False)
    currentlyreading_books = get_currently_reading_books()
    return {
        "toread_books": toread_books,
        "currentlyreading_books": currentlyreading_books
    }

def sync_books(all_books_old, new_toread_and_currentlyreading_books):
    def book_review_is_in_list(book, book_list):
        for bb in book_list:
            if bb['review_id'] == book['review_id']:
                return True
        return False
    def get_book_by_review_id(book_review_id, book_list):
        for bb in book_list:
            if bb['review_id'] == book_review_id:
                return bb
        return None
    def replace_book_in_list(book, book_list):
        for i, bb in enumerate(book_list):
            if bb['review_id'] == book['review_id']:
                book_list[i] = book
                return
    def remove_book_from_list(book, book_list):
        for i, bb in enumerate(book_list):
            if bb['review_id'] == book['review_id']:
                del book_list[i]
                return
    def add_book_to_list(book, book_list):
        book_list.append(book)
    
    for new_to_read_book in new_toread_and_currentlyreading_books[Bookshelf.TO_READ]:
        new_toread_book_in_old_toread = book_review_is_in_list(new_to_read_book, all_books_old[Bookshelf.TO_READ])
        new_toread_book_in_old_currentlyreading = book_review_is_in_list(new_to_read_book, all_books_old[Bookshelf.CURRENTLY_READING])
        new_toread_book_in_old_read = book_review_is_in_list(new_to_read_book, all_books_old[Bookshelf.READ])
        if (
            not new_toread_book_in_old_toread and 
            not new_toread_book_in_old_currentlyreading and 
            not new_toread_book_in_old_read
        ):
            # Case 0: Book is not in any list, add it to to_read
            add_book_to_list(new_to_read_book, all_books_old[Bookshelf.TO_READ])
        elif new_toread_book_in_old_toread:
            # Case 1: Book is already in to_read, replace it with the updated one
            replace_book_in_list(new_to_read_book, all_books_old[Bookshelf.TO_READ])
        elif new_toread_book_in_old_currentlyreading:
            # Case 2: We've stopped reading this book, remove it from currentlyreading and add it to to_read
            remove_book_from_list(new_to_read_book, all_books_old[Bookshelf.CURRENTLY_READING])
            add_book_to_list(new_to_read_book, all_books_old[Bookshelf.TO_READ])
        elif new_toread_book_in_old_read:
            # Case 4: We've read this book, but somehow it's back in to_read
            raise Exception("Book is in old read list but also in new to_read list")
    
    for new_currentlyreading_book in new_toread_and_currentlyreading_books[Bookshelf.CURRENTLY_READING]:
        new_currentlyreading_book_in_old_toread = book_review_is_in_list(
            new_currentlyreading_book, all_books_old[Bookshelf.TO_READ])
        new_currentlyreading_book_in_old_currentlyreading = book_review_is_in_list(
            new_currentlyreading_book, all_books_old[Bookshelf.CURRENTLY_READING])
        new_currentlyreading_book_in_old_read = book_review_is_in_list(
            new_currentlyreading_book, all_books_old[Bookshelf.READ])
        if (
            not new_currentlyreading_book_in_old_toread and 
            not new_currentlyreading_book_in_old_currentlyreading and 
            not new_currentlyreading_book_in_old_read
        ):
            # Case 0: Book is not in any list, add it to currentlyreading
            add_book_to_list(new_currentlyreading_book, all_books_old[Bookshelf.CURRENTLY_READING])
        elif new_currentlyreading_book_in_old_toread:
            # Case 1: Book is already in to_read, remove it from to_read and add it to currentlyreading
            remove_book_from_list(new_currentlyreading_book, all_books_old[Bookshelf.TO_READ])
            add_book_to_list(new_currentlyreading_book, all_books_old[Bookshelf.CURRENTLY_READING])
        elif new_currentlyreading_book_in_old_currentlyreading:
            # Case 2: Book is already in currentlyreading, replace it with the updated one
            replace_book_in_list(new_currentlyreading_book, all_books_old[Bookshelf.CURRENTLY_READING])
        elif new_currentlyreading_book_in_old_read:
            # Case 3: We've read this book, but somehow it's back in currentlyreading
            raise Exception("Book is in old read list but also in new currentlyreading list")

    # Now are there any books in the old currently_reading that are not in the new currently_reading?
    for old_currently_reading_book in all_books_old[Bookshelf.CURRENTLY_READING]:
        old_currently_reading_book_in_new_currently_reading = book_review_is_in_list(
            old_currently_reading_book,
            new_toread_and_currentlyreading_books[Bookshelf.CURRENTLY_READING]
        )
        if not old_currently_reading_book_in_new_currently_reading:
            # Case 5: We've stopped reading this book, remove it from currentlyreading
            remove_book_from_list(old_currently_reading_book, all_books_old[Bookshelf.CURRENTLY_READING])


def run_script(script_name):
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{script_name} executed successfully.")
    else:
        print(f"Error executing {script_name}: {result.stderr}")
    return result.returncode == 0


def main():
    # all_books.json contains the previous data, so load it
    old_all_books = load_json("all_books.json")
    
    # Create a backup of all_books.json as all_books.json.bak
    dict_to_json_file(old_all_books, 'all_books.json.bak')

    # Get toread_books and currentlyreading_books from Goodreads
    toread_and_currentlyreading_books = get_toread_and_currentlyreading_books_from_goodreads()

    # Sync the data (modifies old_all_books in-place)
    sync_books(old_all_books, toread_and_currentlyreading_books)

    # Write updated data to all_books.json
    dict_to_json_file(old_all_books, 'all_books.json')

    # Run 02_all_books_flattener.py to flatten all_books.json into all_books_flat.json
    if run_script('02_all_books_flattener.py'):
        print("Flattening script executed successfully.")
    else:
        print("Flattening script failed.")


    

if __name__ == "__main__":
    main()