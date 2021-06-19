import { Book, F3Bookshelf, Shelf } from "@brombaut/types";
import firebaseConfig from "./firebase.config";

export default class CachedF3Bookshelf {
  private static _instance: F3Bookshelf;
  private static _books: Book[] = [];

  public static async init(): Promise<void> {
    if (!CachedF3Bookshelf._instance) {
      CachedF3Bookshelf._instance = await new F3Bookshelf(firebaseConfig).init();
      this._books = await CachedF3Bookshelf._instance.get();
    }
    return Promise.resolve();
  }

  public static readBooks(): Book[] {
    const readFilter = (book: Book) => book.shelf === Shelf.READ;
    return this._books
      .filter(readFilter)
      .sort(this.sortRecentlyFinishedBooksFirst);
  }

  public static readingBooks(): Book[] {
    const readingFilter = (book: Book) => book.shelf === Shelf.CURRENTLYREADING;
    return this._books
      .filter(readingFilter)
      .sort(this.sortRecentlyStartedBooksFirst);
  }

  public static readBooksGroupedByYear(): { [key: number]: Book[] } {
    const yearlyBooks: { [key: number]: Book[] } = {};
    this.readBookYears().forEach((year: number) => {
      yearlyBooks[year] = [];
    });
    this.readBooks().forEach((book: Book) => {
      yearlyBooks[book.yearFinished].push(book);
    });
    return yearlyBooks;
  }

  private static readBookYears(): number[] {
    const years: number[] = [];
    this.readBooks().forEach((book: Book) => {
      const shouldAdd: boolean = !Number.isNaN(book.yearFinished) && !years.includes(book.yearFinished);
      if (shouldAdd) {
        years.push(book.yearFinished);
      }
    });
    return years.sort((a: number, b: number) => {
      return a - b;
    });
  }

  private static sortRecentlyFinishedBooksFirst(a: Book, b: Book): number {
    return a.compareToDateFinished(b);
  }

  private static sortRecentlyStartedBooksFirst(a: Book, b: Book): number {
    return a.compareToDateStarted(b);
  }

}
