import BookDataParser from "./book-data-parser";
import BookDTO from "./book-dto";

const { parseStringPromise } = require("xml2js");

class BookXmlParser implements BookDataParser {

  async parse(rawData: string): Promise<BookDTO[]> {
    const result = await parseStringPromise(rawData);
    const rawBookList = result.GoodreadsResponse.reviews[0].review;
    const bookList: BookDTO[] = [];
    rawBookList.forEach((review: any) => {
      bookList.push(this.parseBookDto(review));
    });
    return bookList;
  }

  private parseBookDto(review: any): BookDTO {
    // console.log(review);
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
      shelf: review.shelves[0].shelf[0].$.name
    };
    return bookDto;
  }

}

export default BookXmlParser;
