<template>
  <section id="articles">
    <SectionHeader
      title="Articles"
      icon="pen-square"
      subtext="A collection of how-to guides and notes I've written on different topics, mostly so that I can use them as references later."/>
    <div class="section-body">
      <div id="tags-filter" v-if="false">
        <h3 class='header'>Tags Filter</h3>
        <hr>
        <div class="tags-filter__container">
          <Tag v-for="tag in listOfUniqueTags" :key="tag" :tag="tag" />
        </div>
      </div>
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
import Vue from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import ArticleCard from "./ArticleCard.vue";
import Tag from "@/shared/Tag.vue";
import { AuthoredArticlesProxy, AuthoredArticle } from "./AuthoredArticlesProxy";

export default Vue.extend({
  name: "ArticlesSection",
  components: {
    SectionHeader,
    ArticleCard,
    Tag,
  },
  data() {
    return {
      authoredArticles: new AuthoredArticlesProxy().authoredArticles as AuthoredArticle[],
      selectedArticle: null as (AuthoredArticle | null),
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
    listOfUniqueTags(): string[] {
      const arrayOfTagsArrays: string[][] = this.authoredArticles.map((aa: AuthoredArticle) => aa.tags);
      type TagCount = {
        tag: string,
        count: number
      };
      const result: TagCount[] = [];
      arrayOfTagsArrays.forEach((tagsArr: string[]) => {
        tagsArr.forEach((tag: string) => {
          if (!result.find((tc: TagCount) => tc.tag === tag)) {
            result.push({ tag, count: 0 });
          }
          const matchingTC: TagCount | undefined = result.find((tc: TagCount) => tc.tag === tag);
          if (matchingTC) {
            matchingTC.count++;
          }
        });
      });

      return result.map((tc: TagCount) => `${tc.tag} (${tc.count})`);
    },
  },
  methods: {
    articleClicked(article: AuthoredArticle) {
      this.$router.push({ name: "selectedArticle", params: { articleId: article.id } });
      this.selectedArticle = article;
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

    #tags-filter {
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      background-color: darken($secondary, 2%);
      padding: 8px 16px;
      border-radius: 16px;
      margin: 0px 20px;

      .tags-filter__container{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
      }
    }

    .articles-list {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      text-align: left;
      justify-content: center;
    }
  }
}
</style>
