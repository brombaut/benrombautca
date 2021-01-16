import { GoodreadsBookshelf } from "goodreads-bookshelf";
import goodreadsconfig from "./goodreads-config";

export default class CachedBookshelf {
  private static _instance: GoodreadsBookshelf;

  public static async getInstance(callback?: (bs: GoodreadsBookshelf) => void): Promise<void> {
    if (!CachedBookshelf._instance) {
      CachedBookshelf._instance = new GoodreadsBookshelf(goodreadsconfig.id, goodreadsconfig.key);
      await CachedBookshelf._instance.getBooks();
    }
    let t: number;
    const returnLoadedBookShelf = () => {
      if (CachedBookshelf._instance.readBooks().length === 0) {
        t = window.setTimeout(returnLoadedBookShelf, 500);
      } else {
        if (callback) {
          callback(CachedBookshelf._instance);
        }
        window.clearTimeout(t);
      }
    };
    returnLoadedBookShelf();
  }
}
