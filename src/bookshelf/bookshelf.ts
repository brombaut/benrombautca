import Book from "./book";

class Bookshelf {
  private _books: Book[];

  constructor(books: Book[]) {
    this._books = books;
  }

  books(): Book[] {
    return this._books;
  }
}

export default Bookshelf;
