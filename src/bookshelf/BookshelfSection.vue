<template>
  <section id="bookshelf">
    <SectionHeader
      title="Ben's Bookshelf"
      icon="book-open"
      subtext="Books I've read and am currently reading."/>
    <div v-if="booksLoading" class="section-body">
      <div class="loader-wrapper">
        <div class="loader"></div>
      </div>
    </div>
    <div v-else class="section-body">
      <div class="book-group">
        <h2 class='book-group-header'>Currently Reading & Up Next</h2>
        <div class="books">
          <BookCard v-for="book in currentlyReadingAndToReadBooks" :key="book.title" :book="book" />
        </div>
      </div>
      <div v-for="yearBookGroup in readBooksByYear" :key="yearBookGroup.year" class="book-group">
        <h2 class='book-group-header'>{{ yearBookGroup.year }}</h2>
        <div class="books">
          <BookCard v-for="book in yearBookGroup.books" :key="book.title" :book="book" />
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import { Book } from "@brombaut/types";
import SectionHeader from "../shared/SectionHeader.vue";
import BookCard from "./BookCard.vue";
import CachedF3Bookshelf from "./CachedF3Bookshelf";

type YearBooksPair = { year: number; books: Book[] };

export default Vue.extend({
  name: "BookshelfSection",
  components: {
    BookCard,
    SectionHeader,
  },
  data() {
    return {
      booksLoading: true,
      numberOfBookCardsToRow: 6,
    };
  },
  computed: {
    readBooksByYear(): YearBooksPair[] {
      if (this.booksLoading) {
        return [];
      }
      const bookGroups: YearBooksPair[] = [];
      const keyVals = CachedF3Bookshelf.readBooksGroupedByYear();
      Object.entries(keyVals).forEach(keyVal => {
        bookGroups.push({ year: Number(keyVal[0]), books: keyVal[1] });
      });
      return bookGroups.sort((a: YearBooksPair, b: YearBooksPair) => {
        return b.year - a.year;
      });
    },
    currentlyReadingAndToReadBooks(): Book[] {
      if (this.booksLoading) {
        return [];
      }
      const result: Book[] = [...CachedF3Bookshelf.readingBooks(), ...CachedF3Bookshelf.toReadBooks()];
      return result.slice(0, this.numberOfBookCardsToRow);
    },
  },
  methods: {
    async initBookshelf() {
      await CachedF3Bookshelf.init();
      this.booksLoading = false;
    },
    setNumberOfBookCardsToRow() {
      const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
      let result = 6;
      // These were determined manually just by resizing the window until the row broke lol
      if (vw === 0) result = 6;
      if (vw < 1127) result = 5;
      if (vw < 946) result = 4;
      if (vw < 766) result = 3;
      if (vw < 522) result = 2;
      this.numberOfBookCardsToRow = result;
    },
  },
  created() {
    this.initBookshelf();
    this.setNumberOfBookCardsToRow();
    window.addEventListener("resize", this.setNumberOfBookCardsToRow);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.setNumberOfBookCardsToRow);
  },
});
</script>

<style lang="scss">
#bookshelf {
  display: flex;
  flex-direction: column;

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
      width: 100%;

      .book-group-header {
        text-decoration: underline;
        margin-bottom: 4px;
      }

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
