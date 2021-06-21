<template>
  <div class="book-card slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="book.title" />
    </div>
    <h5 class="title">{{ formattedTitle }}</h5>
    <h6 class="author">{{ book.authors.join(' & ') }}</h6>
    <a class="link" :href="book.link" target="_blank">
      On Goodreads
      <font-awesome-icon :icon="['fas', 'external-link-alt']" />
    </a>
    <div v-if="!currentlyReading" class="rating">
      <span v-for="i in bookRating" :key="i" class="star">
        <font-awesome-icon :icon="['fas', 'star']" />
      </span>
    </div>
    <div class='spacer'></div>
    <div v-if="currentlyReading" class="on-page">
      <div class='progress-bar' ref='progressBar'></div>
      <div class='text'>
        On page <span>{{ book.onPage }}</span>/<span>{{ book.numPages }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Book, Shelf } from "@brombaut/types";
import { Component, Vue, Prop } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";

@Component
export default class BookCard extends Vue {
  @Prop()
  book!: Book;

  private bookCardElem!: HTMLDivElement;

  get currentlyReading(): boolean {
    return this.book.shelf === Shelf.CURRENTLYREADING;
  }

  get bookRating(): number {
    return Number(this.book.rating);
  }

  get formattedTitle(): string {
    const { title } = this.book;
    if (title.length < 100) {
      return title;
    }
    const colonIndex = title.indexOf(":");
    if (colonIndex >= 0) {
      return title.substring(0, colonIndex);
    }
    return title;
  }

  get imageSource(): string {
    return `${this.book.isbn13}.jpg`;
  }

  localCheckHorizontalFadeIn() {
    uiUtils.checkHorizontalFadeIn(this.bookCardElem, this.localCheckHorizontalFadeIn);
  }

  setCurrentlyReadingProgressBarIfNecessary() {
    if (!this.currentlyReading) {
      return;
    }
    const progressBarEl = this.$refs.progressBar as HTMLDivElement;
    const percentDone = ((this.book.onPage || 0) / this.book.numPages) * 100;
    progressBarEl.style.width = `${percentDone}%`;
  }

  mounted() {
    this.bookCardElem = this.$el as HTMLDivElement;
    window.addEventListener("scroll", this.localCheckHorizontalFadeIn);
    this.localCheckHorizontalFadeIn();
    this.setCurrentlyReadingProgressBarIfNecessary();
  }
}
</script>

<style lang="scss">

:root{
  --width-to-height-ratio: 0.53;
  --image-width-to-height-ratio: 0.725;
  --card-height-to-image-height-ratio: 0.57;
  --card-height: 360px;
  --card-width: calc(var(--card-height) * var(--width-to-height-ratio));
  --image-height: calc(var(--card-height) * var(--card-height-to-image-height-ratio));
  --image-width: calc(var(--image-height) * var(--image-width-to-height-ratio));
  --small-card-height: 300px;
  --small-card-width: calc(var(--small-card-height) * var(--width-to-height-ratio));
  --small-image-height: calc(var(--small-card-height) * var(--card-height-to-image-height-ratio));
  --small-image-width: calc(var(--small-image-height) * var(--image-width-to-height-ratio));
  --smallest-card-height: 220px;
  --smallest-card-width: calc(var(--smallest-card-height) * var(--width-to-height-ratio));
  --smallest-image-height: calc(var(--smallest-card-height) * var(--card-height-to-image-height-ratio));
  --smallest-image-width: calc(var(--smallest-image-height) * var(--image-width-to-height-ratio));
}

.book-card {
  height: var(--card-height);
  width: var(--card-width);
  display: flex;
  flex-direction: column;
  text-align: left;
  margin: 8px 12px;

  .image-container {
    height: var(--image-height);
    width: var(--image-width);
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
    font-size: 1em;
  }

  .author {
    margin: 4px 0;
    font-size: 1em;
  }

  .spacer {
    flex: 1;
  }

  .on-page {
    background-color: $primaryDark;
    border-radius: 4px;
    padding: 6px 4px;
    position: relative;
    z-index: 0;
    width: var(--image-width);

    .text {
      font-size: 0.8em;
      color: white;
      z-index: 2;
      position: relative;
    }

    .progress-bar {
      position: absolute;
      top: 0;
      left: 0;
      background-color: $primary;
      height: 100%;
      width: 50%;
      border-radius: 4px;
      z-index: 1;
    }
  }

  .rating {
    .star {
      color: $primaryDark;
      font-size: 0.9em;
      margin: 4px 0;
      margin-right: 4px;
    }
  }

  .link {
    margin: 4px 0;
    font-size: 0.7em;
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

  @media only screen and (max-width: 680px) {
    height: var(--small-card-height);
    width: var(--small-card-width);

    .image-container {
      height: var(--small-image-height);
      width: var(--small-image-width);
    }

    .title {
      font-size: 0.8em;
      margin-top: 4px;
      margin-bottom: 2px;
    }

    .author {
      font-size: 0.7em;
      margin: 2px 0;
    }

    .link {
      display: none;
      font-size: 0.6em;
      margin: 2px 0;
    }

    .on-page {
      font-size: 0.8em;
      width: var(--small-image-width);
    }

    .rating {
      .star {
        font-size: 0.7em;
      }
    }
  }

  @media only screen and (max-width: 400px) {
    height: var(--smallest-card-height);
    width: var(--smallest-card-width);

    .image-container {
      height: var(--smallest-image-height);
      width: var(--smallest-image-width);
    }

    .title {
      font-size: 0.5em;
      margin-top: 2px;
      margin-bottom: 0px;
    }

    .author {
      font-size: 0.2em;
      margin: 2px 0;
    }

    .link {
      display: none;
      font-size: 0.3em;
      margin: 0px 0;
    }

    .on-page {
      font-size: 0.4em;
      width: var(--smallest-image-width);
    }

    .rating {
      .star {
        font-size: 0.5em;
      }
    }
  }
}
</style>
