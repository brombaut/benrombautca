<template>
  <section id="articles">
    <SectionHeader title="Articles" icon="pen-square" />
    <div class="section-body">
      <div class="articles-list">
        <ArticleCard
          v-for="article in articlesToDisplay"
          :key="article.id"
          :article="article" />
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import SectionHeader from "../shared/SectionHeader.vue";
import ArticleCard from "./ArticleCard.vue";
import { AuthoredArticlesProxy, AuthoredArticle } from "./AuthoredArticlesProxy";

@Component({
  components: {
    SectionHeader,
    ArticleCard,
  },
})
export default class ArticlesSection extends Vue {
  authoredArticles: AuthoredArticle[];

  constructor() {
    super();
    this.authoredArticles = new AuthoredArticlesProxy().authoredArticles;
  }

  get articlesToDisplay(): AuthoredArticle[] {
    return this.authoredArticles
      .filter((aa: AuthoredArticle) => aa.show)
      .sort((a: AuthoredArticle, b: AuthoredArticle) => {
        return b.createdAt.getTime() - a.createdAt.getTime();
      });
  }

}
</script>

<style lang="scss">
#articles {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: row;
    align-items: center;

    .articles-list {
      display: flex;
      flex-direction: column;
      text-align: left;
      padding: 0 96px; // TODO: Add media queries to reduce this with screen size
    }
  }
}
</style>
