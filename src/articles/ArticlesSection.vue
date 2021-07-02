<template>
  <section id="articles">
    <SectionHeader
      title="Articles"
      icon="pen-square"
      subtext="A collection of how-to guides and notes I've written on different topics, mostly so that I can use them as references later."/>
    <div class="section-body">
      <div class="articles-list">
        <ArticleCard
          v-for="article in articlesToDisplay"
          :key="article.id"
          :article="article"
          @clicked="articleClicked" />
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
  selectedArticle: AuthoredArticle | null;

  constructor() {
    super();
    this.authoredArticles = new AuthoredArticlesProxy().authoredArticles;
    this.selectedArticle = null;
  }

  get articlesToDisplay(): AuthoredArticle[] {
    return this.authoredArticles
      .filter((aa: AuthoredArticle) => aa.show)
      .sort((a: AuthoredArticle, b: AuthoredArticle) => {
        return b.createdAt.getTime() - a.createdAt.getTime();
      });
  }

  articleClicked(article: AuthoredArticle) {
    this.$router.push({ name: "selectedArticle", params: { articleId: article.id } });
    this.selectedArticle = article;
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
    }
  }
}
</style>
