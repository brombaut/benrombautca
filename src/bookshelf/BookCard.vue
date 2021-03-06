<template>
  <div class="book-card slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="book.title()" />
    </div>
    <h5 class="title">{{ formattedTitle }}</h5>
    <h6 class="author">{{ book.author() }}</h6>
    <div v-if="!currentlyReading" class="rating">
      <span v-for="i in bookRating" :key="i" class="star">
        <font-awesome-icon :icon="['fas', 'star']" />
      </span>
    </div>
    <a class="link" :href="book.link()" target="_blank">
      On Goodreads
      <font-awesome-icon :icon="['fas', 'external-link-alt']" />
    </a>
  </div>
</template>

<script lang="ts">
import { Book, Shelf } from "goodreads-bookshelf";
import { Component, Vue, Prop } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";

@Component
export default class BookCard extends Vue {
  @Prop()
  book!: Book;

  private bookCardElem!: HTMLDivElement;

  private imageSource: string = this.book.imageUrl();

  get currentlyReading(): boolean {
    return this.book.shelf() === Shelf.CURRENTLYREADING;
  }

  get bookRating(): number {
    return Number(this.book.rating());
  }

  get formattedTitle(): string {
    const title: string = this.book.title();
    if (title.length < 100) {
      return title;
    }
    const colonIndex = title.indexOf(":");
    if (colonIndex >= 0) {
      return title.substring(0, colonIndex);
    }
    return title;
  }

  localCheckHorizontalFadeIn() {
    uiUtils.checkHorizontalFadeIn(this.bookCardElem, this.localCheckHorizontalFadeIn);
  }

  attemptLocalImageLoad(): void {
    fetch(this.book.localImageUrl())
      .then(response => response.blob())
      .then(blob => {
        if (!blob.type.includes("text/html")) {
          this.imageSource = this.book.localImageUrl();
        }
      });
  }

  mounted() {
    this.bookCardElem = this.$el as HTMLDivElement;
    window.addEventListener("scroll", this.localCheckHorizontalFadeIn);
    this.localCheckHorizontalFadeIn();
    if (this.book.localImageUrl()) {
      this.attemptLocalImageLoad();
    }
  }
}
</script>

<style lang="scss">
.book-card {
  height: 360px;
  width: 190px;
  display: flex;
  flex-direction: column;
  text-align: left;
  margin: 8px 12px;

  .image-container {
    height: 204px;
    width: 148px;
    margin: 4px 0;

    img {
      height: 100%;
      width: 100%;
    }
  }

  .title {
    margin-top: 8px;
    margin-bottom: 4px;
    color: $primary;
    font-size: 1rem;
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

    a {
      margin: 4px 0;
      font-size: 0.7rem;
      color: $primaryDark;

      svg {
        color: $primaryDark !important;
      }

      &:visited {
        color: $primaryDark;
        svg {
          color: $primaryDark;
        }
      }
    }
}
</style>
