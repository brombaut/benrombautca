<template>
  <section id="bookshelf">
    <div class="section-header">
      <font-awesome-icon :icon="['fas', 'book-open']" />
      <h4 class="section-title">BOOKSHELF</h4>
    </div>
    <div class="section-body">
      <BookCard v-for="book in sortedBooks" :key="book.title()" :book="book" />
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import Book from "./book";
import Bookshelf from "./bookshelf";
import BookDataFetcher from "./book-data-fetcher";
import BookDataFileReader from "./book-data-file-reader";
import BookDataParser from "./book-data-parser";
import BookXmlParser from "./book-xml-parser";
import BookshelfBuilder from "./bookshelf-builder";
import BookCard from "./BookCard.vue";
import GoodreadsApiFetcher from "./goodreads-api-fetcher";

@Component({
  components: {
    BookCard
  }
})
export default class BookshelfSection extends Vue {
  private bookshelf: Bookshelf;

  constructor() {
    super();
    this.bookshelf = new Bookshelf([]);
    this.setBookshelf();
  }

  private async setBookshelf() {
    const fetcher: BookDataFetcher = new GoodreadsApiFetcher();
    const parser: BookDataParser = new BookXmlParser();
    const bookshelfBuilder: BookshelfBuilder = new BookshelfBuilder(
      fetcher,
      parser
    );
    this.bookshelf = await bookshelfBuilder.build();
  }

  get readBooks(): Book[] {
    return this.bookshelf.readBooks();
  }

  get currentlyReadingBooks(): Book[] {
    return this.bookshelf.readingBooks();
  }

  get sortedBooks(): Book[] {
    return [...this.currentlyReadingBooks, ...this.readBooks];
  }
}
</script>

<style lang="scss">
#bookshelf {
  display: flex;
  flex-direction: column;

  &:hover {
    .section-header {
      color: $primary;
    }
  }

  .section-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    transition: 0.3s color;

    .section-title {
      margin: 0 8px;
      font-size: 1.2rem;
    }
  }

  .section-body {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}
</style>
