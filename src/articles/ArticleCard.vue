<template>
<div
  class="article-card"
  @click="cardClicked">
  <header>
    <h2 class="title">{{ article.title }}</h2>
  </header>
  <div class='body'>
    <div class="dates">
      Created {{ formatDate(article.createdAt) }} • Updated {{ formatDate(article.updatedAt) }}
    </div>
    <div class="description"><p>{{article.description}}</p></div>
  </div>
  <footer>
    <div class="tags">
      <Tag v-for="tag in article.tags" :key="tag" :tag="tag" />
    </div>
  </footer>
</div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import Tag from "@/shared/Tag.vue";
import { AuthoredArticle } from "./AuthoredArticlesProxy";

export default Vue.extend({
  name: "ArticleCard",
  components: {
    Tag,
  },
  props: {
    article: {
      type: Object as PropType<AuthoredArticle>,
      required: true,
    },
  },
  methods: {
    formatDate(d: Date) {
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
    },
    cardClicked() {
      this.$emit("clicked", this.article);
    },
  },
});
</script>

<style lang='scss'>
$borderRadius: 16px;
$horizontalPadding: 24px;
$verticalPadding: 8px;

.article-card {
  border-radius: $borderRadius;
  margin: 12px 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid $secondaryDark;
  transition: 0.1s;
  flex: 1 1 260px;
  height: 100%;

  header {
    width: calc(100% - 2*$horizontalPadding);
    padding: 2*$verticalPadding $horizontalPadding $verticalPadding $horizontalPadding;
    background-color: $secondaryDark;
    border-top-left-radius: $borderRadius;
    border-top-right-radius: $borderRadius;
  }
  .body {
    width: calc(100% - 2*$horizontalPadding);
    padding: $verticalPadding $horizontalPadding $verticalPadding $horizontalPadding;
    background-color: $secondaryLight;
  }
  footer {
    width: calc(100% - 2*$horizontalPadding);
    padding: $verticalPadding $horizontalPadding 2*$verticalPadding $horizontalPadding;
    background-color: $secondary;
    border-bottom-left-radius: $borderRadius;
    border-bottom-right-radius: $borderRadius;
  }

  &:hover {
    cursor: pointer;
    box-shadow: 0.5px 0.5px 5px $pFontColor;
  }

  .dates {
    margin: 8px 0;
    font-size: 0.9em;
  }

  .title {
    color: $primary;
    font-size: 1.4em;
  }

  .description {
    font-size: 1em;
  }

  .tags {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .article-card {
    margin: 12px 20px;

    .title {
      font-size: 1.5em;
    }
    .description {
      font-size: 0.9em;
    }
  }
}

@media only screen and (max-width: $TINY_DISPLAY_SIZE) {
  .article-card {
    margin: 8px 8px;

    .dates {
      margin: 8px 0;
      font-size: 0.7em;
    }
    .title {
      font-size: 1.2em;
    }
    .description {
      font-size: 0.8em;
    }
  }
}
</style>
