<template>
  <li class="unpublished-publication">
    <div class="publication-card">
      <div class="publication-header">
        <span class="publication-badge unpublished-badge">Unpublished</span>
        <span class="publication-date">{{ unpublishedPublication.month }} {{ unpublishedPublication.year }}</span>
      </div>

      <h4 class="publication-title">{{ unpublishedPublication.title }}</h4>

      <div class="publication-authors">
        <span
          v-for="(a, idx) in unpublishedPublication.authors"
          :key=a
          class="author">
          <span :class="{ 'author-highlight': authorIsBen(a) }">{{ a }}</span><span v-if="idx < unpublishedPublication.authors.length - 1">, </span>
        </span>
      </div>

      <div class="publication-links" v-if="unpublishedPublication.links.length > 0">
        <a
          v-for="link in unpublishedPublication.links"
          :key="link.url"
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer"
          class="publication-link">
          {{ link.type }}
        </a>
      </div>
    </div>
  </li>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import { UnpublishedPublication } from "./types";

export default defineComponent({
  name: "UnpublishedPublication",
  props: {
    unpublishedPublication: {
      type: Object as PropType<UnpublishedPublication>,
      required: true,
    },
    publicationNumber: {
      type: Number,
      required: true,
    },
  },
  methods: {
    authorIsBen(a: string) {
      return a === "Benjamin Rombaut";
    },
  },
});
</script>

<style lang="scss">
.unpublished-publication {
  list-style: none;
  margin-bottom: 20px;

  .publication-card {
    background: white;
    border: 1px solid #e1e4e8;
    border-radius: 8px;
    padding: 20px;
    transition: all 0.2s ease;

    &:hover {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
      border-color: $primary;
    }

    .publication-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;

      .publication-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;

        &.unpublished-badge {
          background-color: #f5f5f5;
          color: #757575;
        }
      }

      .publication-date {
        font-size: 14px;
        color: #666;
      }
    }

    .publication-title {
      font-size: 18px;
      font-weight: 600;
      color: $primary;
      margin: 0 0 12px 0;
      line-height: 1.4;
    }

    .publication-authors {
      font-size: 14px;
      color: #555;
      margin-bottom: 8px;
      line-height: 1.6;

      .author-highlight {
        font-weight: 600;
        color: $primaryDark;
      }
    }

    .publication-links {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;

      .publication-link {
        display: inline-block;
        padding: 6px 14px;
        background-color: #f5f5f5;
        color: $primaryDark;
        text-decoration: none;
        border-radius: 4px;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.2s ease;

        &:hover {
          background-color: $primary;
          color: white;
        }
      }
    }
  }
}

</style>
