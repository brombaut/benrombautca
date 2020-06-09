<template>
  <section id="bookshelf">
    <div class="section-header">
      <font-awesome-icon :icon="['fas', 'book-open']" />
      <h4 class="section-title">BOOKSHELF</h4>
    </div>
    <div class="section-body">
      <div class="book-group">
        <h2>Currently Reading</h2>
        <div class="books">
          <BookCard v-for="book in currentlyReadingBooks" :key="book.title()" :book="book" />
        </div>
      </div>
      <div
        v-for="yearBookGroup in readBooksByYear"
        :key="yearBookGroup.year"
        class="book-group">
        <h2>{{ yearBookGroup.year }}</h2>
        <div class="books">
          <BookCard
            v-for="book in yearBookGroup.books"
            :key="book.title()"
            :book="book" />
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import Book from "./book";
import Bookshelf from "./bookshelf";
import BookCard from "./BookCard.vue";
import CachedBookshelf from "./cached-bookshelf";
import Observer from "./observer";

type YearBooksPair = {year: number, books: Book[]};

@Component({
  components: {
    BookCard
  }
})
export default class BookshelfSection extends Vue implements Observer {
  bookshelf: Bookshelf;

  constructor() {
    super();
    this.bookshelf = CachedBookshelf.getInstance().bookshelf();
    CachedBookshelf.getInstance().registerObserver(this);
  }

  update(bookshelf: Bookshelf): void {
    this.bookshelf = bookshelf;
  }

  get readBooksByYear(): YearBooksPair[] {
    const bookGroups: YearBooksPair[] = [];
    const keyVals = this.bookshelf.readBooksGroupedByYear();
    Object.entries(keyVals).forEach(keyVal => {
      bookGroups.push({ year: Number(keyVal[0]), books: keyVal[1] });
    });
    return bookGroups.sort((a: YearBooksPair, b: YearBooksPair) => {
      if (a.year < b.year) {
        return 1;
      }
      return -1;
    });
  }

  get currentlyReadingBooks(): Book[] {
    return this.bookshelf.readingBooks();
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
    flex-direction: column;
    align-items: flex-start;

    .book-group {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      .books {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        justify-content: flex-start;
        flex-wrap: wrap;
      }
    }
  }
}
</style>
