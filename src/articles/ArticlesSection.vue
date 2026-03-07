<template>
  <section id="articles">
    <SectionHeader
      title="Articles"
      icon="pen-square"
      subtext="A collection of how-to guides and notes I've written on different topics, mostly so that I can use them as references later." />
    <div class="section-body">
      <div v-for="group in articlesByYear" :key="group.year" class="year-group">
        <div class="year-label">{{ group.year }}</div>
        <div
          v-for="article in group.articles"
          :key="article.id"
          class="article-row"
          role="button"
          tabindex="0"
          @click="articleClicked(article)"
          @keydown.enter="articleClicked(article)">
          <div class="article-title">{{ article.title }}</div>
          <div class="article-meta">
            <span class="article-date">{{ formatDate(article.createdAt) }}</span>
            <span v-if="article.description" class="article-description"> &middot; {{ article.description }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import { AuthoredArticlesProxy, AuthoredArticle } from "./AuthoredArticlesProxy";

interface YearGroup {
  year: number;
  articles: AuthoredArticle[];
}

export default defineComponent({
  name: "ArticlesSection",
  components: {
    SectionHeader,
  },
  data() {
    return {
      authoredArticles: new AuthoredArticlesProxy().authoredArticles as AuthoredArticle[],
    };
  },
  computed: {
    articlesToDisplay(): AuthoredArticle[] {
      return this.authoredArticles
        .filter((aa: AuthoredArticle) => aa.show && !aa.archived)
        .sort((a: AuthoredArticle, b: AuthoredArticle) => {
          return b.createdAt.getTime() - a.createdAt.getTime();
        });
    },
    articlesByYear(): YearGroup[] {
      const groups: { [year: number]: AuthoredArticle[] } = {};
      this.articlesToDisplay.forEach((article: AuthoredArticle) => {
        const year = article.createdAt.getFullYear();
        if (!groups[year]) groups[year] = [];
        groups[year].push(article);
      });
      return Object.keys(groups)
        .map(Number)
        .sort((a, b) => b - a)
        .map(year => ({ year, articles: groups[year] }));
    },
  },
  methods: {
    articleClicked(article: AuthoredArticle) {
      this.$router.push({ name: "selectedArticle", params: { articleId: article.id } });
    },
    formatDate(d: Date) {
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getMonth()]} ${d.getDate()}`;
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
    width: 100%;
  }

  .year-group {
    margin-bottom: 32px;
  }

  .year-label {
    font-size: 0.85em;
    font-weight: 700;
    color: $hFontColor;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding-bottom: 8px;
    border-bottom: 2px solid $secondaryDark;
    margin-bottom: 4px;
  }

  .article-row {
    padding: 14px 8px;
    border-bottom: 1px solid $secondaryDark;
    cursor: pointer;
    transition: background-color 0.1s;

    &:hover {
      background-color: $secondaryLight;

      .article-title {
        color: $primary;
      }
    }
  }

  .article-title {
    font-size: 1.05em;
    font-weight: 600;
    color: $fontColor;
    margin-bottom: 4px;
    line-height: 1.4;
  }

  .article-meta {
    font-size: 0.82em;
    color: $silver;
  }

  .article-description {
    font-style: italic;
  }
}
</style>
