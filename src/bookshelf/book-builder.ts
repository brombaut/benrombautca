import Book from "./book";
import BookDTO from "./book-dto";

class BookBuilder {
  private _bookDto: BookDTO;

  constructor(_bookDto: BookDTO) {
    this._bookDto = _bookDto;
  }

  build(): Book {
    console.log(this._bookDto.title, " - ", this._bookDto.isbn13);
    return new Book(this._bookDto);
  }

  private buildOpenLibraryImageUrl(size: string): string {
    return `http://covers.openlibrary.org/b/isbn/${this._bookDto.isbn}-${size}.jpg`;
  }
}

export default BookBuilder;
