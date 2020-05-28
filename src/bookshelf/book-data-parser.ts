import BookDTO from "./book-dto";

interface BookDataParser {
  parse(rawData: string): Promise<BookDTO[]>;
}

export default BookDataParser;
