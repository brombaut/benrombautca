<template>
<div
  class="article-card"
  @click="cardClicked">
  <div class="dates">
    Created {{ formatDate(article.createdAt) }} • Updated {{ formatDate(article.updatedAt) }}
  </div>
  <h2 class="title">{{ article.title }}</h2>
  <div class="description"><p>{{article.description}}</p></div>
  <div class="tags">
    <Tag v-for="tag in article.tags" :key="tag" :tag="tag" />
  </div>
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
.article-card {
  background-color: $secondary;
  border-radius: 16px;
  margin: 12px 20px;
  padding: 24px 32px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid $secondaryDark;
  transition: 0.1s;

  &:hover {
    cursor: pointer;
    box-shadow: 1px 1px 5px $pFontColor;
  }

  .dates {
    margin: 8px 0;
    font-size: 0.9em;
  }

  .title {
    color: $primary;
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
    padding: 12px 24px;

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
    padding: 8px 16px;

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
