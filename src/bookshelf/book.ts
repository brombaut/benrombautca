import BookDTO from "./book-dto";
import Shelf from "./shelf";

class Book {
  private _title: string;
  private _author: string;
  private _isbn: string;
  private _imageUrl: string;
  private _smallImageUrl: string;
  private _largeImageUrl: string;
  private _link: string;
  private _dateStarted: string;
  private _dateFinished: string;
  private _rating: string;
  private _shelf: Shelf;

  constructor(bookDto: BookDTO) {
    this._title = bookDto.title;
    this._author = bookDto.author;
    this._isbn = bookDto.isbn;
    this._imageUrl = bookDto.imageUrl;
    this._smallImageUrl = bookDto.smallImageUrl;
    this._largeImageUrl = bookDto.largeImageUrl;
    this._link = bookDto.link;
    this._dateStarted = bookDto.dateStarted;
    this._dateFinished = bookDto.dateFinished;
    this._rating = bookDto.rating;
    this._shelf = bookDto.shelf;
  }

}

export default Book;
