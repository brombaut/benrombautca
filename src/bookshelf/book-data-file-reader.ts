import BookDataFetcher from "./book-data-fetcher";

class BookDataFileReader implements BookDataFetcher {
  async fetch() {
    return new Promise((resolve, reject) => {
      const rawFile = new XMLHttpRequest();
      rawFile.open("GET", "goodreads-response.xml", true);
      rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
          const allText = rawFile.responseText;
          resolve(allText);
        }
      };
      rawFile.send();
    });
  }
}

export default BookDataFileReader;
