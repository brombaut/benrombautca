<template>
  <div class="publication-card">
    <div class="publication-year-badge">{{ journal.year }}</div>
    <div class="publication-content">
      <h4 class="publication-title">{{ journal.title }}</h4>
      <div class="publication-meta">
        <span class="publication-authors">{{ formattedAuthors }}</span>
      </div>
      <div class="publication-venue">{{ journal.venue }}</div>
      <div class="publication-links">
        <a
          v-for="link in journal.links"
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
import { JournalPublication } from "./types";

export default defineComponent({
  name: "JournalPublication",
  props: {
    journal: {
      type: Object as PropType<JournalPublication>,
      required: true,
    },
    publicationNumber: {
      type: Number,
      required: true,
    },
  },
  computed: {
    formattedAuthors(): string {
      const { authors } = this.journal;
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
