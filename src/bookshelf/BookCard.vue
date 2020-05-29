<template>
  <div class="book-card slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="book.title()" />
    </div>
    <h5 class="title">{{ book.title() }}</h5>
    <h6 class="author">{{ book.author() }}</h6>
    <div v-if="currentlyReading" class="currently-reading">Currently Reading</div>
    <div v-else class="rating">
      <span v-for="i in bookRating" :key="i" class="star">
        <font-awesome-icon :icon="['fas', 'star']" />
      </span>
    </div>
    <div class="link-container">
      <a class="link" :href="book.link()" target="_blank">
        On Goodreads
        <font-awesome-icon :icon="['fas', 'external-link-alt']" />
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import Book from "./book";
import Shelf from "./shelf";

@Component
export default class BookCard extends Vue {
  @Prop()
  book!: Book;

  private bookCardElem!: HTMLDivElement;

  get imageSource(): string {
    return this.book.imageUrl();
  }

  get currentlyReading(): boolean {
    return this.book.shelf() === Shelf.CURRENTLYREADING;
  }

  get bookRating(): number {
    return Number(this.book.rating());
  }

  localCheckHorizontalFadeIn() {
    uiUtils.checkHorizontalFadeIn(
      this.bookCardElem,
      this.localCheckHorizontalFadeIn
    );
  }

  mounted() {
    this.bookCardElem = this.$el as HTMLDivElement;
    window.addEventListener("scroll", this.localCheckHorizontalFadeIn);
    this.localCheckHorizontalFadeIn();
  }
}
</script>

<style lang="scss">
.book-card {
  height: 320px;
  width: 180px;
  display: flex;
  flex-direction: column;
  text-align: left;
  margin: 8px 12px;

  .image-container {
    height: 170px;
    width: 132px;
    margin: 4px 0;
    // max-width: calc(100vw - 56px);

    img {
      height: 100%;
      width: 100%;
    }
  }

  .title {
    margin-top: 8px;
    margin-bottom: 4px;
    color: $primary;
  }

  .author {
    margin: 4px 0;
  }

  .star,
  .currently-reading {
    color: $primaryDark;
    font-size: 0.8rem;
    margin: 4px 0;
  }

  .rating {
    .star {
      margin-right: 4px;
    }
  }

  .link-container {
    background: $secondaryLightest;
    color: white;
    padding: 4px 8px;
    width: fit-content;
    border-radius: 4px;
    margin: 4px 0;
    transition: filter 0.3s;
    display: flex;
    align-items: center;

    &:hover {
      cursor: pointer;
      filter: brightness(80%);
    }

    a {
      font-size: 0.7rem;

      svg {
        color: white !important;
      }

      &:visited {
        color: inherit;
        svg {
          color: inherit;
        }
      }
    }
  }
}
</style>
