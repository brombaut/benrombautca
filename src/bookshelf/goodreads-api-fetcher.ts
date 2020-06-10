import BookDataFetcher from "./book-data-fetcher";

class GoodreadsApiFetcher implements BookDataFetcher {
  async fetch() {
    const proxyUrl = "https://cors-anywhere.herokuapp.com/";
    const url = "https://www.goodreads.com/review/list?v=2&key=mlNe4pqsW02fhvEOKxu7mg&id=115130270&per_page=200";
    return fetch(`${proxyUrl}${url}`)
      .then(res => res.text());
  }
}

export default GoodreadsApiFetcher;
