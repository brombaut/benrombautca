import Bookshelf from "./bookshelf";

interface Observer {
  update(bookshelf: Bookshelf): void;
}

export default Observer;
