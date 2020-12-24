import { GoodreadsBookshelf } from "goodreads-bookshelf";
import goodreadsconfig from "./goodreads-config";

export default class CachedBookshelf {
  private static _instance: GoodreadsBookshelf;

  public static async getInstance(): Promise<GoodreadsBookshelf> {
    if (!CachedBookshelf._instance) {
      CachedBookshelf._instance = new GoodreadsBookshelf(goodreadsconfig.id, goodreadsconfig.key);
      await CachedBookshelf._instance.getBooks();
    }
    return Promise.resolve(CachedBookshelf._instance);
  }
}
