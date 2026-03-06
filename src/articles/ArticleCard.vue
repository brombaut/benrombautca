<template>
  <div
    class="article-card"
    role="button"
    tabindex="0"
    @click="cardClicked"
    @keydown.enter="cardClicked">
    <header>
      <h2 class="title">{{ article.title }}</h2>
    </header>
    <div class='body'>
      <div class="dates">
        Created {{ formatDate(article.createdAt) }} • Updated {{ formatDate(article.updatedAt) }}
      </div>
      <div class="description"><p>{{article.description}}</p></div>
    </div>
  </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import { AuthoredArticle } from "./AuthoredArticlesProxy";

export default defineComponent({
  name: "ArticleCard",
  components: {},
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
  &:hover {
    $darkenPercent: 4%;
    cursor: pointer;

    header {
      background-color: darken($secondaryDark, $darkenPercent);
    }

    body {
      background-color: darken($secondaryLight, $darkenPercent);
    }
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
