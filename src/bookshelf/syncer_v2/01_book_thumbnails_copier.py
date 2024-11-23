import json
import os
import shutil

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def find_f3_book(f3_books, review_id):
    for f3_book in f3_books:
        if f3_book['goodreads_review_id'] == review_id:
            return f3_book
    return None

def main():
    unhandled_books = []
    books_to_handle = []
    # load all_books.json
    all_books = load_json("all_books.json")
    all_books = all_books['toread_books'] + all_books['read_books'] + all_books['currentlyreading_books']
    # load f3Books.json
    f3_books = load_json("../syncer/f3Books.json")
    # For every book in all_books, check find the associated book in f3_books based on the review_id
    # If the book is found, copy the thumbnail_url to the all_books entry
    for book in all_books:
        review_id = str(book['review_id'])
        f3_book = find_f3_book(f3_books, review_id)
        if not f3_book:
            unhandled_books.append(book)
        else:
            book["isbn13"] = f3_book["isbn13"]
            books_to_handle.append(book)
    unknown_isbn13 = []
    for book in books_to_handle:
        # Make copy of jpg file stored in "../book-thumbails/{book["isbn13"]}.jpg" to "./book-thumbnails_v2/{book["review_id"]}.jpg"
        try:
            source_dir = "../book-thumbnails"
            destination_dir = "./book_thumbnails_v2"
            source_file = os.path.join(source_dir, f"{book['isbn13']}.jpg")
            # destination_file = os.path.join(destination_dir, f"{book['review_id']}.jpg")
            destination_file = os.path.join(destination_dir, f"{book['book_id']}.jpg")
            shutil.copyfile(source_file, destination_file)
        except FileNotFoundError:
            unknown_isbn13.append(book['isbn13'])
            print(f"Unknown isbn13: {book['isbn13']}")


if __name__ == "__main__":
    main()