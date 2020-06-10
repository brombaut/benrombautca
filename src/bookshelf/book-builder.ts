import Book from "./book";
import BookDTO from "./book-dto";

class BookBuilder {
  private _bookDto: BookDTO;

  constructor(_bookDto: BookDTO) {
    this._bookDto = _bookDto;
  }

  build(): Book {
    return new Book(this._bookDto);
  }
}

export default BookBuilder;
