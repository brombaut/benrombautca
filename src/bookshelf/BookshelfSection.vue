<template>
  <section id="bookshelf">
    <SectionHeader
      title="Ben's Bookshelf"
      icon="book-open"
      subtext="Books I've read and am currently reading." />
    <div class="section-body">
      <div class="book-group">
        <h2 class='book-group-header'>Currently Reading & Up Next</h2>
        <div class="books">
          <BookCard
            v-for="book in currentlyReadingAndToReadBooks"
            :key="book.review_id"
            :book="book"
            :shouldHidePercentText="shouldHidePercentText" />
        </div>
      </div>
      <div v-for="yearBookGroup in readBooksByYear" :key="yearBookGroup.year" class="book-group">
        <hr>
        <div class="book-group-header">
          <h2 class='year-header'>{{ yearBookGroup.year }}</h2>
        </div>
        <div class="books">
          <BookCard v-for="book in yearBookGroup.books" :key="book.review_id" :book="book" />
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import BookCard from "./BookCard.vue";
import booksData from "./syncer_v2/all_books_flattened.json";

interface Book {
    title: string;
    author: string;
    book_id: string;
    review_id: number;
    shelf: string;
}

interface ToReadBook extends Book {
    date_added: string;
    position: number;
}

interface CurrentlyReadingBook extends Book {
    date_added: string;
    onPage: number;
    numPages: number;
}

interface ReadBook extends Book {
    date_finished: string;
    rating: number;
}

type YearBooksPair = {
  year: number;
  books: Book[];
};

export default defineComponent({
  name: "BookshelfSection",
  components: {
    BookCard,
    SectionHeader,
  },
  data() {
    return {
      numberOfBookCardsToRow: 6,
      shouldHidePercentText: false,
    };
  },
  computed: {
    readBooksByYear(): YearBooksPair[] {
      const typedBooksData = booksData as Book[];
      const readBooksSorted: ReadBook[] = typedBooksData.filter((book) => book.shelf === "read") as ReadBook[];
      readBooksSorted.sort((a, b) => {
        return new Date(b.date_finished ?? 0).getTime() - new Date(a.date_finished ?? 0).getTime();
      });
      const bookGroups: YearBooksPair[] = [];
      readBooksSorted.forEach((book: ReadBook) => {
        const year = new Date(book.date_finished ?? 0).getFullYear();
        const yearGroup = bookGroups.find((group) => group.year === year);
        if (yearGroup) {
          yearGroup.books.push(book);
        } else {
          bookGroups.push({
            year,
            books: [book],
          });
        }
      });
      const sortedByYear: YearBooksPair[] = bookGroups.sort(
        (a: YearBooksPair, b: YearBooksPair) => {
          return b.year - a.year;
        },
      );
      return sortedByYear;
    },
    currentlyReadingAndToReadBooks(): Book[] {
      const typedBooksData = booksData as Book[];
      const currentlyReadingBooks: CurrentlyReadingBook[] = typedBooksData.filter((book) => book.shelf === "currently-reading") as CurrentlyReadingBook[];
      currentlyReadingBooks.sort((a, b) => {
        if (!a.date_added) return -1;
        if (!b.date_added) return 1;
        return new Date(a.date_added).getTime() - new Date(b.date_added).getTime();
      });
      const toReadBooks: ToReadBook[] = typedBooksData
        .filter((book) => book.shelf === "to-read") as ToReadBook[];
      toReadBooks.sort((a, b) => {
        if (!a.position) return -1;
        if (!b.position) return 1;
        return a.position - b.position;
      });

      const combined = [...currentlyReadingBooks, ...toReadBooks];
      return combined.slice(0, this.numberOfBookCardsToRow);
    },
  },
  methods: {
    setNumberOfBookCardsToRow() {
      const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
      let result = 6;
      // These were determined manually just by resizing the window until the row broke lol
      if (vw === 0) result = 6;
      if (vw < 1127) result = 5;
      if (vw < 946) result = 4;
      if (vw < 766 && vw >= 640) result = 3;
      if (vw < 640 && vw >= 600) result = 4;
      if (vw < 600 && vw >= 550) result = 3;
      if (vw < 550 && vw >= 480) result = 4;
      if (vw < 480) result = 3;
      if (vw < 370) result = 2;
      this.numberOfBookCardsToRow = result;
    },
    setShouldHidePercentText() {
      const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
      this.shouldHidePercentText = vw < 640;
    },
  },
  created() {
    this.setNumberOfBookCardsToRow();
    this.setShouldHidePercentText();
    window.addEventListener("resize", this.setNumberOfBookCardsToRow);
    window.addEventListener("resize", this.setShouldHidePercentText);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.setNumberOfBookCardsToRow);
    window.removeEventListener("resize", this.setShouldHidePercentText);
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
