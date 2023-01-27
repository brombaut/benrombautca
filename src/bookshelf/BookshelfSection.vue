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
        <hr>
        <div class="book-group-header">
          <h2 class='year-header'>{{ yearBookGroup.year }}</h2>
          <ProgressBar
            v-if="yearBookGroup.yearGoal"
            text="Yearly Goal:"
            :numer="yearBookGroup.books.length"
            :denom="yearBookGroup.yearGoal"
            :hidePercent="true" />
        </div>
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
import ProgressBar from "./ProgressBar.vue";

type YearBooksPair = {
  year: number;
  books: Book[];
  yearGoal: number;
};

export default Vue.extend({
  name: "BookshelfSection",
  components: {
    BookCard,
    SectionHeader,
    ProgressBar,
  },
  data() {
    const yearGoals: {[key: number]: number} = {
      2021: 52,
      2022: 26,
      2023: 20,
    };
    return {
      booksLoading: true,
      numberOfBookCardsToRow: 6,
      yearGoals,
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
        const year = Number(keyVal[0]);
        bookGroups.push({
          year,
          books: keyVal[1],
          yearGoal: this.yearGoals[year],
        });
      });
      const sortedByYear: YearBooksPair[] = bookGroups.sort((a: YearBooksPair, b: YearBooksPair) => {
        return b.year - a.year;
      });
      return sortedByYear;
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

      hr {
        height: 2px;
        width: 100%;
        background-color: $primaryDark;
      }

      .book-group-header {
        margin-bottom: 12px;
        display: flex;

        .year-header {
          text-decoration: underline;
          margin-right: 8px;
        }
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
