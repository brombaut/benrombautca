import Bookshelf from "./bookshelf";
import BookDataFetcher from "./book-data-fetcher";
import GoodreadsApiFetcher from "./goodreads-api-fetcher";
import BookDataParser from "./book-data-parser";
import BookXmlParser from "./book-xml-parser";
import BookshelfBuilder from "./bookshelf-builder";
import BookDataFileReader from "./book-data-file-reader";
import Subject from "./subject";
import Observer from "./observer";

class CachedBookshelf implements Subject {
  private static _instance: CachedBookshelf;
  private _bookshelf: Bookshelf = new Bookshelf([]);
  private _observers: Observer[] = [];

  registerObserver(o: Observer): void {
    this._observers.push(o);
  }

  removeObserver(toRemove: Observer): void {
    this._observers = this._observers.filter((o: Observer) => o !== toRemove);
  }

  notifyObservers(): void {
    this._observers.forEach((o: Observer) => o.update(this._bookshelf));
  }

  public static getInstance(): CachedBookshelf {
    if (!CachedBookshelf._instance) {
      CachedBookshelf._instance = new CachedBookshelf();
      CachedBookshelf._instance.init();
    }
    return CachedBookshelf._instance;
  }

  private async init() {
    // const fetcher: BookDataFetcher = new BookDataFileReader();
    const fetcher: BookDataFetcher = new GoodreadsApiFetcher();
    const parser: BookDataParser = new BookXmlParser();
    const bookshelfBuilder: BookshelfBuilder = new BookshelfBuilder(
      fetcher,
      parser
    );
    this._bookshelf = await bookshelfBuilder.build();
    this.notifyObservers();
  }

  bookshelf(): Bookshelf {
    return this._bookshelf;
  }
}

export default CachedBookshelf;
