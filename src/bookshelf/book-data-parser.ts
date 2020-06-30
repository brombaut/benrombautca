import BookDTO from "./book-dto";

interface BookDataParser {
  booklist(): BookDTO[];
  parse(rawData: string): Promise<void>;
  done(): boolean;
}

export default BookDataParser;
