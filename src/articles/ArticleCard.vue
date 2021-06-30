<template>
<div class="article-card">
  <div class="dates">
    Created {{ formatDate(article.createdAt) }} • Updated {{ formatDate(article.updatedAt) }}
  </div>
  <h2 class="title">{{ article.title }}</h2>
  <div class="description"><p>{{article.description}}</p></div>
  <div class="tags">
    <div
      v-for="tag in article.tags"
      :key=tag
      class="tag">{{ tag }}</div>
  </div>
</div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import { AuthoredArticle } from "./AuthoredArticlesProxy";

@Component
export default class ArticleCard extends Vue {

  @Prop()
  article!: AuthoredArticle;

  formatDate(d: Date) {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  }
}
</script>

<style lang='scss'>
.article-card {
  background-color: $secondary;
  border-radius: 16px;
  margin: 12px 20px;
  padding: 24px 32px;
  max-width: 692px;
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

    .tag {
      font-size: 0.8em;
      margin-right: 4px;
      padding: 8px 12px;
      border-radius: 8px;
      color: $secondary;
      background-color: $primaryDark;
    }
  }
}
</style>
