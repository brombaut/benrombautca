<template>
  <section id="selected-article">
    <SectionHeader :title="selectedArticle.title" icon="" :subtext="selectedArticle.description"/>
    <div class="meta-container">
      <div class="dates">
        Created {{ formatDate(selectedArticle.createdAt) }} • Updated {{ formatDate(selectedArticle.updatedAt) }}
      </div>
      <div class="tags">
        <Tag v-for="tag in selectedArticle.tags" :key="tag" :tag="tag" />
      </div>
    </div>
    <div class="section-body">
      <GitHubMarkdown :content="selectedArticle.body" />
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SectionHeader from "../shared/SectionHeader.vue";
import Tag from "../shared/Tag.vue";
import GitHubMarkdown from "../shared/GitHubMarkdown.vue";
import { AuthoredArticlesProxy, AuthoredArticle } from "./AuthoredArticlesProxy";

@Component({
  components: {
    SectionHeader,
    Tag,
    GitHubMarkdown,
  },
})
export default class ArticlesSection extends Vue {
  selectedArticleId: string;
  selectedArticle: AuthoredArticle | null;

  constructor() {
    super();
    window.scrollTo(0, 0);
    this.selectedArticleId = this.$router.currentRoute.params.articleId;
    this.selectedArticle = this.loadSelectedArticle(this.selectedArticleId);

  }

  loadSelectedArticle(aId: string): AuthoredArticle | null {
    const allArticles: AuthoredArticle[] = new AuthoredArticlesProxy().authoredArticles;
    const selectedArticle: AuthoredArticle | undefined = allArticles.find((aa: AuthoredArticle) => aa.id === aId);
    return selectedArticle || null;
  }

  formatDate(d: Date) {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  }

  backToArticles() {
    this.$router.push({ name: "articles" });
  }
}
</script>

<style lang="scss">
#selected-article {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  .section-header {
    margin-bottom: 4px;

    .section-title {
      line-height: 1.5em;
    }
  }

  .meta-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 16px;

    .dates {
      margin: 0px 0;
    }

    .tags {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      margin: 8px 0;
    }

  }

  .section-body {
    text-align: left;
    width: 100%;
  }
}

</style>
