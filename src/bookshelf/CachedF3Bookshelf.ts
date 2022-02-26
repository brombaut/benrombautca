import { Book, F3Bookshelf, Shelf } from "@brombaut/types";
import firebaseConfig from "./firebase.config";

export default class CachedF3Bookshelf {
  private static _instance: F3Bookshelf;
  private static _books: Book[] = [];
  private static _loading = false;

  public static async init(): Promise<void> {
    if (!CachedF3Bookshelf._instance) {
      try {
        CachedF3Bookshelf._loading = true;
        CachedF3Bookshelf._instance = new F3Bookshelf(firebaseConfig);
        await CachedF3Bookshelf._instance.init();
        this._books = await CachedF3Bookshelf._instance.get();
      } finally {
        CachedF3Bookshelf._loading = false;
      }
    }

    while (CachedF3Bookshelf._loading) {
      await new Promise(r => setTimeout(r, 500));
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

  public static toReadBooks(): Book[] {
    const toReadFilter = (book: Book) => book.shelf === Shelf.TOREAD;
    return this._books
      .filter(toReadFilter)
      .sort((a: Book, b: Book) => {
        if (!a.toReadOrder) return -1;
        if (!b.toReadOrder) return 1;
        return a.toReadOrder - b.toReadOrder;
      });
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
