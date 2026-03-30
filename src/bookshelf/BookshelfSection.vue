<template>
  <section id="bookshelf">
    <SectionHeader
      title="Ben's Bookshelf"
      icon="book-open"
      subtext="Books I've read and am currently reading." />
    <div class="section-body">
      <div class="book-group">
        <h2 class='book-group-header'>Currently Reading</h2>
        <div class="books">
          <BookCard
            v-for="book in currentlyReadingBooks"
            :key="book.link"
            :book="book" />
        </div>
      </div>
      <div v-for="yearBookGroup in readBooksByYear" :key="yearBookGroup.year" class="book-group">
        <hr>
        <div class="book-group-header">
          <h2 class='year-header'>{{ yearBookGroup.year }}</h2>
        </div>
        <div class="books">
          <BookCard v-for="book in yearBookGroup.books" :key="book.link" :book="book" />
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
    link: string;
    shelf: string;
}

interface CurrentlyReadingBook extends Book {
    date_added: string;
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
  computed: {
    readBooksByYear(): YearBooksPair[] {
      const typedBooksData = booksData as Book[];
      const readBooksSorted: ReadBook[] = typedBooksData.filter((book) => book.shelf === "read") as ReadBook[];
      readBooksSorted.sort((a, b) => {
        const dateA = new Date(a.date_finished ?? 0);
        const dateB = new Date(b.date_finished ?? 0);
        const timeA = Number.isNaN(dateA.getTime()) ? 0 : dateA.getTime();
        const timeB = Number.isNaN(dateB.getTime()) ? 0 : dateB.getTime();
        return timeB - timeA;
      });
      const bookGroups: YearBooksPair[] = [];
      readBooksSorted.forEach((book: ReadBook) => {
        const year = this.extractYear(book.date_finished);
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
    currentlyReadingBooks(): Book[] {
      const typedBooksData = booksData as Book[];
      const currentlyReadingBooks: CurrentlyReadingBook[] = typedBooksData.filter((book) => book.shelf === "currently-reading") as CurrentlyReadingBook[];
      currentlyReadingBooks.sort((a, b) => {
        if (!a.date_added) return -1;
        if (!b.date_added) return 1;
        return new Date(a.date_added).getTime() - new Date(b.date_added).getTime();
      });
      return currentlyReadingBooks;
    },
  },
  methods: {
    extractYear(dateString: string | undefined): number {
      if (!dateString) {
        return new Date().getFullYear();
      }

      // Try to parse the date normally
      const date = new Date(dateString);
      if (!Number.isNaN(date.getTime())) {
        return date.getFullYear();
      }

      // If parsing failed, try to extract year with regex
      // Matches 4-digit years (e.g., "2025" from "Dec 31, 2025")
      const yearMatch = dateString.match(/\b(19|20)\d{2}\b/);
      if (yearMatch) {
        return parseInt(yearMatch[0], 10);
      }

      // Final fallback to current year
      return new Date().getFullYear();
    },
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
