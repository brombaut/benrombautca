import Book from "./book";
import BookDTO from "./book-dto";

class BookBuilder {
  private _bookDto: BookDTO;

  constructor(_bookDto: BookDTO) {
    this._bookDto = _bookDto;
  }

  build(): Book {
    if (this._bookDto.smallImageUrl.includes("nophoto")) {
      // console.log("No Small Photo - ", this._bookDto.title);
      const isValidIsbn = /^\d+$/.test(this._bookDto.isbn);
      if (isValidIsbn) {
        // console.log("UPDATING SMALL Title: ", this._bookDto.title, " ISBN - ", this._bookDto.isbn);
        this._bookDto.smallImageUrl = this.buildOpenLibraryImageUrl("S");
      } else {
        // console.log("SMALL Title: ", this._bookDto.title, " ISBN - ", this._bookDto.isbn);
      }
    }

    if (this._bookDto.imageUrl.includes("nophoto")) {
      // console.log("No Med Photo - ", this._bookDto.title);
      const isValidIsbn = /^\d+$/.test(this._bookDto.isbn);
      if (isValidIsbn) {
        this._bookDto.imageUrl = this.buildOpenLibraryImageUrl("M");
      } else {
        // console.log("MEDIUM Title: ", this._bookDto.title, " ISBN - ", this._bookDto.isbn);
      }
    }
    // console.log("ISBN - ", this._bookDto.isbn);
    return new Book(this._bookDto);
  }

  private buildOpenLibraryImageUrl(size: string): string {
    return `http://covers.openlibrary.org/b/isbn/${this._bookDto.isbn}-${size}.jpg`;
  }
}

export default BookBuilder;
