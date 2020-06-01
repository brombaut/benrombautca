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
import BookCard from "./BookCard.vue";
import CachedBookshelf from "./cached-bookshelf";
import Observer from "./observer";

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
