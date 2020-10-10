import BookDTO from "./book-dto";
import Shelf from "./shelf";

class Book {
  private _title: string;
  private _author: string;
  private _isbn: string;
  private _isbn13: string;
  private _imageUrl: string;
  private _smallImageUrl: string;
  private _largeImageUrl: string;
  private _link: string;
  private _dateStarted: Date;
  private _dateFinished: Date;
  private _rating: string;
  private _shelf: Shelf;

  constructor(bookDto: BookDTO) {
    this._title = bookDto.title;
    this._author = bookDto.author;
    this._isbn = bookDto.isbn;
    this._isbn13 = bookDto.isbn13;
    this._imageUrl = bookDto.imageUrl;
    this._smallImageUrl = bookDto.smallImageUrl;
    this._largeImageUrl = bookDto.largeImageUrl;
    this._link = bookDto.link;
    this._dateStarted = this.parseDate(bookDto.dateStarted);
    this._dateFinished = this.parseDate(bookDto.dateFinished);
    this._rating = bookDto.rating;
    this._shelf = bookDto.shelf;
  }

  private parseDate(input: string) {
    const parts = input.split(" ");
    const monthIndex = this.monthIndex(parts[1]);
    const day = Number(parts[2]);
    const year = Number(parts[5]);
    return new Date(year, monthIndex, day);
  }

  private monthIndex(monthAbbr: string): number {
    const months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    return months.findIndex((a: string) => a === monthAbbr);
  }

  title(): string {
    return this._title;
  }

  author(): string {
    return this._author;
  }

  imageUrl(): string {
    return this._imageUrl;
  }

  localImageUrl(): string {
    return this._isbn13 ? `${this._isbn13}.jpg` : "";
  }

  link(): string {
    return this._link;
  }

  dateStarted(): Date {
    return this._dateStarted;
  }

  dateFinished(): Date {
    return this._dateFinished;
  }

  yearFinished(): number {
    return this._dateFinished.getFullYear();
  }

  rating(): string {
    return this._rating;
  }

  shelf(): Shelf {
    return this._shelf;
  }
}

export default Book;
