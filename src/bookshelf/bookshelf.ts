import Book from "./book";
import Shelf from "./shelf";

class Bookshelf {
  private _books: Book[];

  constructor(books: Book[]) {
    this._books = books;
  }

  private sortRecentlyFinishedBooksFirst(a: Book, b: Book): number {
    if (a.dateFinished() < b.dateFinished()) {
      return 1;
    }
    return -1;
  }

  private sortRecentlyStartedBooksFirst(a: Book, b: Book): number {
    if (a.dateStarted() < b.dateStarted()) {
      return 1;
    }
    return -1;
  }

  readBooks(): Book[] {
    return this._books
      .filter((book: Book) => book.shelf() === Shelf.READ)
      .sort(this.sortRecentlyFinishedBooksFirst);
  }

  readingBooks(): Book[] {
    return this._books
      .filter((book: Book) => book.shelf() === Shelf.CURRENTLYREADING)
      .sort(this.sortRecentlyStartedBooksFirst);
  }
}

export default Bookshelf;
