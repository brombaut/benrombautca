import BookDataFetcher from "./book-data-fetcher";

class GoodreadsApiFetcher implements BookDataFetcher {
  private _version = 2;
  private _key = "mlNe4pqsW02fhvEOKxu7mg";
  private _id = 115130270;
  private _perPage = 199;
  private _page = 1;

  async fetch() {
    const proxyUrl = "https://cors-anywhere.herokuapp.com/";
    return fetch(`${proxyUrl}${this.url}`).then(res => res.text());
  }

  incrementPage(): void {
    this._page++;
  }

  private get url() {
    return `https://www.goodreads.com/review/list?v=${this._version}&key=${this._key}&id=${this._id}&per_page=${this._perPage}&page=${this._page}`;
  }
}

export default GoodreadsApiFetcher;
