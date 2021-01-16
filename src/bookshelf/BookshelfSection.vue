<template>
  <section id="bookshelf">
    <SectionHeader title="BEN'S BOOKSHELF" icon="book-open" />
    <div v-if="loadingBookshelf" class="section-body">
      <div class="loader-wrapper">
        <div class="loader"></div>
      </div>
    </div>
    <div v-else class="section-body">
      <div class="book-group">
        <h2>Currently Reading</h2>
        <div class="books">
          <BookCard v-for="book in currentlyReadingBooks" :key="book.title()" :book="book" />
        </div>
      </div>
      <div v-for="yearBookGroup in readBooksByYear" :key="yearBookGroup.year" class="book-group">
        <h2>{{ yearBookGroup.year }}</h2>
        <div class="books">
          <BookCard v-for="book in yearBookGroup.books" :key="book.title()" :book="book" />
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { Book, GoodreadsBookshelf } from "goodreads-bookshelf";
import { Component, Vue, Watch } from "vue-property-decorator";
import SectionHeader from "../shared/SectionHeader.vue";
import BookCard from "./BookCard.vue";
import CachedBookshelf from "./cached-bookshelf";

type YearBooksPair = { year: number; books: Book[] };

@Component({
  components: {
    BookCard,
    SectionHeader,
  },
})
export default class BookshelfSection extends Vue {
  bookshelf!: GoodreadsBookshelf;
  booksLoading = true;

  constructor() {
    super();
    this.loadingBookshelf = true;
    this.initBookshelf();
  }

  initBookshelf() {
    const callback = (grBookshelf: GoodreadsBookshelf) => {
      this.bookshelf = grBookshelf;
      this.$nextTick().then(() => {
        this.loadingBookshelf = false;
      });
    };
    CachedBookshelf.getInstance(callback);
  }

  set loadingBookshelf(val: boolean) {
    this.booksLoading = val;
  }

  get loadingBookshelf(): boolean {
    return this.booksLoading;
  }

  get readBooksByYear(): YearBooksPair[] {
    if (this.loadingBookshelf) {
      return [];
    }
    const bookGroups: YearBooksPair[] = [];
    const keyVals = this.bookshelf.readBooksGroupedByYear();
    Object.entries(keyVals).forEach(keyVal => {
      bookGroups.push({ year: Number(keyVal[0]), books: keyVal[1] });
    });
    return bookGroups.sort((a: YearBooksPair, b: YearBooksPair) => {
      return b.year - a.year;
    });
  }

  get currentlyReadingBooks(): Book[] {
    console.log(this.loadingBookshelf);
    if (this.loadingBookshelf) {
      return [];
    }
    return this.bookshelf.readingBooks();
  }
}
</script>

<style lang="scss">
#bookshelf {
  display: flex;
  flex-direction: column;

  .section-header {
    display: flex;
    flex-direction: column;
    padding: 16px 0;
    width: fit-content;
    margin-bottom: 16px;

    .section-header_content {
      display: flex;
      flex-direction: row;
      transition: 0.3s color;
      font-size: 2rem;
      align-items: center;
      line-height: 2;

      .section-title {
        margin: 0 16px;
      }
    }

    .section-header-underline {
      background: $primary;
      height: 4px;
    }
  }

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    .loader-wrapper {
      width: 100%;
      display: flex;
      justify-content: center;

      .loader {
        border: 16px solid $primaryDarkest;
        border-top: 16px solid $primary;
        border-bottom: 16px solid $primary;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        animation: spin 1s linear infinite;
      }

      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    }

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
