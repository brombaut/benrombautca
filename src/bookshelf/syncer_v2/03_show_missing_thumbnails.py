import json
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def file_exists(file_path):
    return os.path.exists(file_path)

def main():
    all_books_flattened_json_file_path = os.path.join(script_dir, "all_books_flattened.json")
    all_books = load_json(all_books_flattened_json_file_path)
    missing_thumbnails = []
    for book in all_books:
        thumbnail_path = os.path.join(script_dir, "book_thumbnails_v2", f"{book['book_id']}.webp")
        if not file_exists(thumbnail_path):
            missing_thumbnails.append(book)
    print(f"Missing thumbnails:")
    for mt in missing_thumbnails:
        print(f"{mt['title']} -- {mt['author']} -- {mt['book_id']}")


if __name__ == "__main__":
    main()