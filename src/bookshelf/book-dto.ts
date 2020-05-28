import Shelf from "./shelf";

interface BookDTO {
  title: string;
  author: string;
  isbn: string;
  isbn13: string;
  imageUrl: string;
  smallImageUrl: string;
  largeImageUrl: string;
  link: string;
  dateStarted: string;
  dateFinished: string;
  rating: string;
  shelf: Shelf;
}

export default BookDTO;
