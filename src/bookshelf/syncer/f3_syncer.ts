import * as fs from "fs";
import { Book, F3Bookshelf, FirestoreBook, Shelf } from "@brombaut/types";
import { FirestoreDateTranslator, FirebaseConfigurer } from "firebase-firestore-facade";
import * as dotenv from "dotenv";

dotenv.config();

const PARSE_INT_RADIX = 10;

const firebaseConfig: FirebaseConfigurer = {
  apiKey: process.env.VUE_APP_API_KEY || "",
  authDomain: process.env.VUE_APP_AUTH_DOMAIN || "",
  projectId: process.env.VUE_APP_PROJECT_ID || "",
  storageBucket: process.env.VUE_APP_STORAGE_BUCKET || "",
  messagingSenderId: process.env.VUE_APP_MESSAGING_SENDER_ID || "",
  appId: process.env.VUE_APP_APP_ID || "",
  measurementId: process.env.VUE_APP_MEASUREMENT_ID || "",
  auth: {
    email: process.env.VUE_APP_TEST_USER_EMAIL || "",
    password: process.env.VUE_APP_TEST_USER_PASSWORD || "",
  },
};

interface GRBook {
  title: string,
  short_title: string,
  authors:string,
  isbn13: string,
  link: string,
  num_pages: number | null,
  dateStarted: string | null,
  dateFinished: string | null,
  rating: string,
  shelf: Shelf,
  goodreads_review_id: string,
  on_page: number | null,
  to_read_order: number | null
}

async function main() {
  console.log("Starting Sync");
  console.log("Init F3Bookshelf");
  const f3: F3Bookshelf = await new F3Bookshelf(firebaseConfig).init();

  console.log("Reading translated goodreads book file");
  const booksFromGoodreads: GRBook[] = readTranslatedBooksFile();

  console.log("Fetching existing F3 books");
  const f3Books: Book[] = await fetchF3Books(f3);

  console.log("Syncing existing F3 books");
  const existingF3Books = syncExistingF3Books(f3Books, booksFromGoodreads);

  console.log("Updating F3 with synced books");
  await updateF3WithSyncedBooks(f3, existingF3Books);

  console.log("Creating new F3 books");
  const newF3Books = createNewF3Books(f3Books, booksFromGoodreads);

  console.log("Updating F3 with added books");
  await addNewBooksToF3(f3, newF3Books);

  console.log("Closing F3 Connection");
  await f3.closeConnection();

  console.log("Done");
}

function readTranslatedBooksFile() {
  // TODO: Make the working directory a command line argument or env var
  const data = fs.readFileSync("./src/bookshelf/syncer/translated_books_from_gr.json", "utf8");
  return JSON.parse(data);
}

async function fetchF3Books(f3: F3Bookshelf): Promise<Book[]> {
  const books: Book[] = await f3.get();
  return books;
}

function syncExistingF3Books(f3Books: Book[], grBooks: GRBook[]): Book[] {
  /**
   * This function will return a list of F3 books that need to be synced.
   * We check a list of cases (see below), and based on which cases evaluate to true,
   * we update the Book with the correct data (from the associated GRBook),
   * and add it to the list to be returned.
   *
   * Case 1 - Both records are still to read and the toReadOrder value has changed
   * Case 2 - We have started reading a book that was previously toRead.
   * Case 3 - We have finished reading a book we were previously reading.
   * Case 4 - A book has a higher onPage value.
   * Case 5 - A book has a different rating value.
   *
   * Note that if we are re-reading a book, the previous record will have a "@X" suffix
   * on the goodreads_review_id, which means it will never match here.
   *
   * We also handle creation of a new record of a book that is being re-read in the createNewF3Books function
   */
  const result: Book[] = [];
  f3Books.forEach((b: Book) => {
    const grBook: GRBook | undefined = grBooks.find((grb: GRBook) => grb.goodreads_review_id === b.goodreads_review_id);
    if (!grBook) return;
    let needsSyncing = false;

    // Case 1 - Both records are still to read...
    // the only thing that might have changed that needs updating
    // is the toReadOrder value
    if (grBook.shelf == Shelf.TOREAD && b.shelf == Shelf.TOREAD) {
      const toReadOrderIsNotMagicNumber = grBook.to_read_order !== 99;
      const toReadOrderNumbersDoNotMatch = grBook.to_read_order !== b.toReadOrder
      if (toReadOrderIsNotMagicNumber && toReadOrderNumbersDoNotMatch) {
        b.toReadOrder = grBook.to_read_order;
        needsSyncing = true;
      }
    }

    // Case 2 - We have started reading a book that was previously toRead.
    if (grBook.shelf == Shelf.CURRENTLYREADING && b.shelf == Shelf.TOREAD) {
      b.startReading();
      needsSyncing = true;
    }

    // Case 3 - We have finished reading a book we were previously reading
    if (grBook.shelf == Shelf.READ && b.shelf == Shelf.CURRENTLYREADING) {
      b.finishedReading();
      needsSyncing = true;
    }

    // Case 4 - A book has a higher onPage value
    if (b.onPage !== null && grBook.on_page !== null) {
      const changedAndGROnPageIsHigher = b.onPage !== grBook.on_page && grBook.on_page > b.onPage;
      if (changedAndGROnPageIsHigher) {
        b.onPage = grBook.on_page;
        needsSyncing = true;
      }
    }

    // Case 5 - A book has a different rating value
    if (b.rating !== parseInt(grBook.rating, PARSE_INT_RADIX)) {
      b.rating = parseInt(grBook.rating, PARSE_INT_RADIX);
      needsSyncing = true;
    }

    const grIsbnIsDifferentThanF3 = grBook.isbn13 && b.isbn13 !== grBook.isbn13;
    if (grIsbnIsDifferentThanF3) {
      console.warn(`WARNING - ReviewID=${b.goodreads_review_id} title=${b.title} :: ISBN13 do not match :: f3.isbn13=${b.isbn13} gr.isbn13=${grBook.isbn13}`);
    }
    if (needsSyncing) {
      // FIXME: This toReadOrder field was added later,
      // and now causes problems when GoodReads updates
      // their books that I had read before I added the field.
      // For those books, just make it 99 magic number.
      // Realistically, this will probably never be fixed.
      if (!b.toReadOrder) {
        b.toReadOrder = 99;
      }
      result.push(b);
    }
  });
  return result;
}

async function updateF3WithSyncedBooks(f3: F3Bookshelf, syncedF3Books: Book[]) {
  for (const b of syncedF3Books) {
    await f3.put(b);
  }
}

function createNewF3Books(f3Books: Book[], grBooks: GRBook[]): FirestoreBook[] {
  /**
   * We will create new F3 Book records for Goodreads Books who have a goodreads_review_id
   * that does not exist in our F3 database.
   *
   * This also will handle creating new "re-read" book records, since we should have manually
   * added a "@X" suffix to the goodreads_review_id in F3 for the book we have started re-reading.
   */
  const newGRBooks: GRBook[] = [];
  grBooks.forEach((grb: GRBook) => {
    // We dont have a goodreads_review_id for the GoodReads book in our F3 database
    let i = f3Books.findIndex((b: Book) => b.goodreads_review_id === grb.goodreads_review_id);
    if (i < 0) {
      newGRBooks.push(grb);
    }
  });

  const newFirestoreBooks: FirestoreBook[] = newGRBooks.map((grb: GRBook) => {
    // We are re-reading a book if the GoodReads good is currently-reading and
    // we have a goodreads_review_id with the "@X" suffix removed record existing in our database.
    const previousReviewIdRecordExists = f3Books.findIndex((b: Book) => b.goodreads_review_id.split("@")[0] === grb.goodreads_review_id) >= 0;
    const isReRead = previousReviewIdRecordExists && grb.shelf === Shelf.CURRENTLYREADING;
    let sDate = null;
    if (isReRead) {
      sDate = new FirestoreDateTranslator().fromDate(new Date()).toFirestoreDate();
    } else if (grb.dateStarted) {
      sDate = new FirestoreDateTranslator().fromDate(new Date(grb.dateStarted)).toFirestoreDate();
    }
    let fDate = null;
    if (!isReRead && grb.dateFinished) {
      fDate = new FirestoreDateTranslator().fromDate(new Date(grb.dateFinished)).toFirestoreDate();
    }
    return {
      id: "",
      goodreads_review_id: grb.goodreads_review_id,
      isbn13: grb.isbn13,
      title: grb.title,
      shortTitle: grb.short_title,
      authors: [grb.authors],
      numPages: grb.num_pages || 0,
      link: grb.link,
      shelf: grb.shelf,
      onPage: grb.on_page,
      dateStarted: sDate,
      dateFinished: fDate,
      rating: isReRead ? 0 : parseInt(grb.rating, PARSE_INT_RADIX),
      toReadOrder: grb.to_read_order ? grb.to_read_order : 99,
    };
  });
  return newFirestoreBooks;
}

async function addNewBooksToF3(f3: F3Bookshelf, newBooks: FirestoreBook[]) {
  for (const fb of newBooks) {
    await f3.post(fb);
  }
}

main();
