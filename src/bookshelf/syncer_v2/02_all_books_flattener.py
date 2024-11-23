import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def write_json_to_file(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    all_books = load_json("all_books.json")
    flattened = []
    for book_type in all_books:
        for book in all_books[book_type]:
            if book_type == "toread_books":
                book["shelf"] = "to-read"
            elif book_type == "read_books":
                book["shelf"] = "read"
            else:
                book["shelf"] = "currently-reading"
            flattened.append(book)
    write_json_to_file(flattened, "all_books_flattened.json")


if __name__ == "__main__":
    main()