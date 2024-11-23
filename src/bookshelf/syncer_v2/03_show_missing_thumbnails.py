import json
import os


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def file_exists(file_path):
    return os.path.exists(file_path)

def main():
    all_books = load_json("all_books_flattened.json")
    missing_thumbnails = []
    for book in all_books:
        thumbnail_path = f"./book_thumbnails_v2/{book['book_id']}.jpg"
        if not file_exists(thumbnail_path):
            missing_thumbnails.append(book)
    print(f"Missing thumbnails:")
    for mt in missing_thumbnails:
        print(f"{mt['title']} -- {mt['author']} -- {mt['book_id']}")


if __name__ == "__main__":
    main()