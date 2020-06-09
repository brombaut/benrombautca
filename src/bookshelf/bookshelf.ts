import Book from "./book";
import Shelf from "./shelf";

class Bookshelf {
  private _books: Book[];

  constructor(books: Book[]) {
    this._books = books;
  }

  public readBooks(): Book[] {
    return this._books
      .filter((book: Book) => book.shelf() === Shelf.READ)
      .sort(this.sortRecentlyFinishedBooksFirst);
  }

  public readingBooks(): Book[] {
    return this._books
      .filter((book: Book) => book.shelf() === Shelf.CURRENTLYREADING)
      .sort(this.sortRecentlyStartedBooksFirst);
  }

  public readBooksGroupedByYear(): { [key: number]: Book[] } {
    const yearlyBooks: { [key: number]: Book[] } = {};
    this.readBookYears().forEach((year: number) => {
      yearlyBooks[year] = [];
    });
    this.readBooks().forEach((book: Book) => {
      yearlyBooks[book.yearFinished()].push(book);
    });
    return yearlyBooks;
  }

  private readBookYears(): number[] {
    const years: number[] = [];
    this.readBooks().forEach((book: Book) => {
      if (Number.isNaN(book.yearFinished())) {
        return;
      }
      if (years.includes(book.yearFinished())) {
        return;
      }
      years.push(book.yearFinished());
    });
    return years.sort((a: number, b: number) => {
      if (a > b) {
        return 1;
      }
      return -1;
    });
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
}

export default Bookshelf;
