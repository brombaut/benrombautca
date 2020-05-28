import BookDataFetcher from "./book-data-fetcher";
import BookDataParser from "./book-data-parser";
import Bookshelf from "./bookshelf";
import BookBuilder from "./book-builder";
import Book from "./book";
import BookDTO from "./book-dto";

class BookshelfBuilder {
  private _dataFetcher: BookDataFetcher;

  private _dataParser: BookDataParser;

  constructor(fetcher: BookDataFetcher, parser: BookDataParser) {
    this._dataFetcher = fetcher;
    this._dataParser = parser;
  }

  async build(): Promise<Bookshelf> {
    const rawData: string = await this._dataFetcher.fetch();
    const jsonBooks: BookDTO[] = await this._dataParser.parse(rawData);
    const books: Book[] = [];
    jsonBooks.forEach((bj: BookDTO) => {
      const bookBuilder: BookBuilder = new BookBuilder(bj);
      books.push(bookBuilder.build());
    });
    console.log(books);
    return new Bookshelf(books);
  }
}

export default BookshelfBuilder;
