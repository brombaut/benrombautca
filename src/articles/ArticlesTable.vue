<template>
  <table class="articles-table">
    <thead>
      <tr>
        <th>{{articles.length}} Articles</th>
        <th>Tags</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="article in articles"
        :key="article.id"
        @click="() => cardClicked(article)">
        <td class="info-column">
          <div class="main"><b>{{article.title}}</b></div>
          <div class="secondary">
            Created {{ formatDate(article.createdAt) }} •
            Updated {{ formatDate(article.updatedAt) }}
          </div>
        </td>
        <td class="tags-column">
          <Tag v-for="tag in article.tags" :key="tag" :tag="tag" />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import Tag from "@/shared/Tag.vue";
import { AuthoredArticle } from "./AuthoredArticlesProxy";

export default defineComponent({
  name: "ArticlesTable",
  components: {
    Tag,
  },
  props: {
    articles: {
      type: Array as PropType<AuthoredArticle[]>,
      required: true,
    },
  },
  methods: {
    formatDate(d: Date) {
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
    },
    cardClicked(article: AuthoredArticle) {
      this.$emit("clicked", article);
    },
  },
});
</script>

<style lang='scss'>

.articles-table {
  border-collapse: collapse;
  thead {
    background-color: $secondaryDarkest;
    border: 1px solid $secondaryDark;
    color: $hFontColor;
    tr {
      th {
        padding: 12px 12px 6px 20px;
      }
    }
  }
  tbody {
    background-color: $secondary;

    tr {
      border: 1px solid $secondaryDark;

      &:nth-child(2n) {
        background-color: $secondaryLight;
      }

      td {
        padding: 8px 20px;
      }

      .info-column {
        .main {
          font-size: 1.2em;
          margin-bottom: 6px;
        }
        .secondary {
          font-size: 0.8em;
          margin-top: 6px;
        }
      }

      .tags-column {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
      }

      &:hover {
        background-color: $secondaryDark;
        cursor: pointer;
      }
    }
  }
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .articles-table{
    tbody {
      tr {
        td {
          padding: 6px 16px;
        }
        .info-column {
          .main {
            font-size: 1em;
            margin-bottom: 4px;
          }
          .secondary {
            font-size: 0.8em;
            margin-top: 4px;
          }
        }
      }
    }
  }
}

@media only screen and (max-width: $TINY_DISPLAY_SIZE) {
    .articles-table{
    tbody {
      tr {
        td {
          padding: 4px 12px;
        }
        .info-column {
          .main {
            font-size: 0.8em;
            margin-bottom: 4px;
          }
          .secondary {
            font-size: 0.6em;
            margin-top: 4px;
          }
        }
      }
    }
  }
}
</style>
