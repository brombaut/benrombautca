<template>
  <section id="articles">
    <SectionHeader
      title="Articles"
      icon="pen-square"
      subtext="A collection of how-to guides and notes I've written on different topics, mostly so that I can use them as references later." />
    <div class="section-body">
      <div class="articles-table-container" v-if="tableView">
        <ArticlesTable
          :articles=articlesToDisplay
          @clicked="articleClicked" />
      </div>
      <div class="articles-cards-container" v-else>
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
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import ArticleCard from "./ArticleCard.vue";
import ArticlesTable from "./ArticlesTable.vue";
import { AuthoredArticlesProxy, AuthoredArticle } from "./AuthoredArticlesProxy";

export default defineComponent({
  name: "ArticlesSection",
  components: {
    SectionHeader,
    ArticleCard,
    ArticlesTable,
  },
  data() {
    return {
      tableView: true,
      authoredArticles: new AuthoredArticlesProxy().authoredArticles as AuthoredArticle[],
    };
  },
  computed: {
    articlesToDisplay(): AuthoredArticle[] {
      return this.authoredArticles
        .filter((aa: AuthoredArticle) => aa.show)
        .sort((a: AuthoredArticle, b: AuthoredArticle) => {
          return b.createdAt.getTime() - a.createdAt.getTime();
        });
    },
  },
  methods: {
    articleClicked(article: AuthoredArticle) {
      this.$router.push({ name: "selectedArticle", params: { articleId: article.id } });
    },
  },
});
</script>

<style lang="scss">
#articles {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    .articles-cards-container {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      text-align: left;
      justify-content: center;
    }
  }
}
</style>
