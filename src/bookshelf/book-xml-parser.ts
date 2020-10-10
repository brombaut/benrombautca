import BookDataParser from "./book-data-parser";
import BookDTO from "./book-dto";

const { parseStringPromise } = require("xml2js");

interface Pagination {
  start: string;
  end: string;
  total: string;
}

class BookXmlParser implements BookDataParser {
  private readonly _bookList: BookDTO[];
  private _done: boolean;

  constructor() {
    this._bookList = [];
    this._done = false;
  }

  done(): boolean {
    return this._done;
  }

  public booklist() {
    return this._bookList;
  }

  async parse(rawData: string): Promise<void> {
    const result = await parseStringPromise(rawData);
    const rawReviewStruct = result.GoodreadsResponse.reviews[0];
    const rawBookList = rawReviewStruct.review;
    rawBookList.forEach((review: any) => {
      this._bookList.push(this.parseBookDto(review));
    });
    this.checkIfDone(rawReviewStruct.$);
  }

  private parseBookDto(review: any): BookDTO {
    const bookDto = {
      title: review.book[0].title[0],
      author: review.book[0].authors[0].author[0].name[0],
      isbn: review.book[0].isbn[0],
      isbn13: review.book[0].isbn13[0],
      imageUrl: review.book[0].image_url[0],
      smallImageUrl: review.book[0].image_url[0],
      largeImageUrl: review.book[0].large_image_url[0],
      link: review.book[0].link[0],
      dateStarted: review.date_added[0],
      dateFinished: review.read_at[0],
      rating: review.rating[0],
      shelf: review.shelves[0].shelf[0].$.name,
    };
    if (typeof bookDto.isbn === "object") {
      bookDto.isbn = "";
    }
    if (typeof bookDto.isbn13 === "object") {
      bookDto.isbn13 = "";
    }
    return bookDto;
  }

  private checkIfDone(page: Pagination) {
    try {
      this._done = Number(page.end) >= Number(page.total);
    } catch {
      this._done = true;
    }
  }

}

export default BookXmlParser;
