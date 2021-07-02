<template>
  <section id="selected-article">
    <!-- <div class='back-button-container'>
      <button class='button' @click="backToArticles">
        <font-awesome-icon class='icon' :icon="['fas', 'chevron-left']"/>
        <span>All Articles</span>
      </button>
    </div> -->
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
      <div class="article-content github-markdown-style" v-html="selectedArticle.body"></div>
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SectionHeader from "../shared/SectionHeader.vue";
import Tag from "../shared/Tag.vue";
import { AuthoredArticlesProxy, AuthoredArticle } from "./AuthoredArticlesProxy";

@Component({
  components: {
    SectionHeader,
    Tag,
  },
})
export default class ArticlesSection extends Vue {
  selectedArticleId: string;
  selectedArticle: AuthoredArticle | null;
  resizeListeners: number[] = [];

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

  // NOTE: Should move this to UI utils so software page can use it.
  // Yes definitly...youll have to figure out all these timeouts
  resizeSourceCodeEl(preCodeEl: HTMLPreElement): void {
    preCodeEl.style.width = "";
    setTimeout(() => {
      if (!preCodeEl.parentElement) return;
      const { width: parentWidth } = preCodeEl.parentElement.getBoundingClientRect();
      const oneSidePadding = 20;
      preCodeEl.style.width = `${parentWidth - (oneSidePadding * 2)}px`;
    }, 0);
  }

  resizeAllCodeEls() {
    const preCodeEls: NodeListOf<HTMLPreElement> = this.$el.querySelectorAll("pre.sourceCode");
    preCodeEls.forEach((preCodeEl: HTMLPreElement) => {
      this.resizeSourceCodeEl(preCodeEl);
    });
  }

  mounted() {
    this.resizeAllCodeEls();
    window.addEventListener("resize", this.resizeAllCodeEls);
  }

  beforeUnmount() {
    window.removeEventListener("resize", this.resizeAllCodeEls);
  }

}
</script>

<style lang="scss">
@import "@/styles/github_article.scss";

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
      margin: 0px 12px;
    }

    .tags {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      margin: 8px;
    }

  }

  .section-body {
    text-align: left;
    width: 100%;
  }
}

</style>
