import subprocess
import requests
from bs4 import BeautifulSoup


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

def get_toread_and_currentlyreading_books_from_goodreads():
    toread_books = get_books_for_shelf("to-read", parse_toread_books_from_html, debug=False)
    currentlyreading_books = get_currently_reading_books()
    return {
        "to_read": toread_books,
        "currently_reading": currentlyreading_books
    }


def run_script(script_name):
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{script_name} executed successfully.")
    else:
        print(f"Error executing {script_name}: {result.stderr}")
    return result.returncode == 0


def main():
    # all_books.json contains the previous data, so load it
    all_books_old = load_json("all_books.json")
    
    # Create a backup of all_books.json as all_books.json.bak
    dict_to_json_file(all_books_old, 'all_books.json.bak')

    # Get toread_books and currentlyreading_books from Goodreads
    toread_and_currentlyreading_books = get_toread_and_currentlyreading_books_from_goodreads()

    # Write new_all_books.json to all_books.json
    dict_to_json_file(toread_and_currentlyreading_books, 'all_books.json')

    # Run 02_all_books_flattener.py to flatten all_books.json into all_books_flat.json
    if run_script('02_all_books_flattener.py'):
        print("Flattening script executed successfully.")
    else:
        print("Flattening script failed.")


    

if __name__ == "__main__":
    main()