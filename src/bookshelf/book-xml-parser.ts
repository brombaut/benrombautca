import BookDataParser from "./book-data-parser";
import BookDTO from "./book-dto";

const { parseStringPromise } = require("xml2js");

class BookXmlParser implements BookDataParser {

  async parse(rawData: string): Promise<BookDTO[]> {
    const result = await parseStringPromise(rawData);
    const rawBookList = result.GoodreadsResponse.reviews[0].review;
    const bookList: BookDTO[] = [];
    rawBookList.forEach((raw: any) => {
      bookList.push({
        title: raw.book[0].title[0],
        author: raw.book[0].authors[0].author[0].name[0],
        isbn: raw.book[0].isbn[0],
        imageUrl: raw.book[0].image_url[0],
        smallImageUrl: raw.book[0].image_url[0],
        largeImageUrl: raw.book[0].large_image_url[0],
        link: raw.book[0].link[0],
        dateStarted: raw.date_added[0],
        dateFinished: raw.read_at[0],
        rating: raw.rating[0],
        shelf: raw.shelves[0].shelf[0].$.name
      });
    });
    return bookList;
  }

}

export default BookXmlParser;
