<template>
  <div class="publication-card">
    <div class="publication-year-badge">{{ unpublishedPublication.year }}</div>
    <div class="publication-content">
      <h4 class="publication-title">{{ unpublishedPublication.title }}</h4>
      <div class="publication-meta">
        <span class="publication-authors">{{ formattedAuthors }}</span>
      </div>
      <div class="publication-links">
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
  </div>
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
  computed: {
    formattedAuthors(): string {
      const { authors } = this.unpublishedPublication;
      if (authors.length === 1) {
        return authors[0];
      }
      if (authors.length === 2) {
        return `${authors[0]} and ${authors[1]}`;
      }
      return `${authors[0]} et al.`;
    },
  },
});
</script>

<style lang="scss">
</style>
