<template>
  <div class="publication-card">
    <div class="publication-year-badge">{{ conference.year }}</div>
    <div class="publication-content">
      <h4 class="publication-title">{{ conference.title }}</h4>
      <div class="publication-meta">
        <span class="publication-authors">{{ formattedAuthors }}</span>
      </div>
      <div class="publication-venue">{{ conference.conferenceName }}</div>
      <div class="publication-links">
        <a
          v-for="link in conference.links"
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
import { ConferencePublication } from "./types";

export default defineComponent({
  name: "ConferencePublication",
  props: {
    conference: {
      type: Object as PropType<ConferencePublication>,
      required: true,
    },
    publicationNumber: {
      type: Number,
      required: true,
    },
  },
  computed: {
    formattedAuthors(): string {
      const { authors } = this.conference;
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
