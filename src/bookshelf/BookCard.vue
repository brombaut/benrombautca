<template>
  <div class="book-card slide-in" :class="{'to-read': toRead}">
    <div class="image-container">
      <img :src="imageSource" :alt="book.book_id" />
    </div>
    <h5 class="title">{{ formattedTitle }}</h5>
    <h6 class="author">{{ book.author }}</h6>
    <div v-if="toRead" class="up-next-label">
      <span>Up Next</span>
    </div>
    <ProgressBar
      v-if="currentlyReading"
      text="On page"
      :numer="Number(book.onPage)"
      :denom="Number(book.numPages)"/>
    <div v-if="read" class="rating">
      <span v-for="i in bookRating" :key="i" class="star">
        <font-awesome-icon :icon="['fas', 'star']" />
      </span>
    </div>
  </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
// import { Book, Shelf } from "@brombaut/types";
import uiUtils from "@/utils/ui-utils";
import ProgressBar from "./ProgressBar.vue";

export default defineComponent({
  name: "BookCard",
  props: {
    book: {
      type: Object as PropType<any>,
      required: true,
    },
  },
  components: {
    ProgressBar,
  },
  computed: {
    toRead(): boolean {
      return this.book.shelf === "to-read";
    },
    currentlyReading(): boolean {
      return this.book.shelf === "currently-reading";
    },
    read(): boolean {
      return this.book.shelf === "read";
    },
    bookRating(): number {
      return Number(this.book.rating);
    },
    formattedTitle(): string {
      const { title } = this.book;
      if (title.length < 100) {
        return title;
      }
      const colonIndex = title.indexOf(":");
      if (colonIndex >= 0) {
        return title.substring(0, colonIndex);
      }
      return title;
    },
    imageSource(): string {
      return `book_thumbnails_v2/${this.book.book_id}.jpg`
    },
  },
  methods: {
    localCheckHorizontalFadeIn() {
      uiUtils.checkHorizontalFadeIn(this.$el as HTMLDivElement, this.localCheckHorizontalFadeIn);
    },
  },
  mounted() {
    window.addEventListener("scroll", this.localCheckHorizontalFadeIn);
    this.localCheckHorizontalFadeIn();
  },
});
</script>

<style lang="scss">

:root{
  --width-to-height-ratio: 0.52;
  --image-width-to-height-ratio: 0.725;
  --card-height-to-image-height-ratio: 0.57;
  --card-height: 340px;
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
  margin: 0 2px;

  &.to-read {
    filter: brightness(60%);
  }

  .image-container {
    height: var(--image-height);
    width: var(--image-width);
    margin: 2px 0;

    img {
      height: 100%;
      width: 100%;
    }
  }

  .title {
    margin-top: 4px;
    margin-bottom: 2px;
    color: $primary;
    font-size: 0.9em;
  }

  .author {
    margin: 2px 0;
    font-size: 0.8em;
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

  .up-next-label {
    font-size: 0.8em;
  }

  @media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
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

    .rating {
      .star {
        font-size: 0.7em;
      }
    }
  }

  @media only screen and (max-width: $PHONE_DISPLAY_SIZE) {
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

    .rating {
      .star {
        font-size: 0.5em;
      }
    }
  }
}
</style>
