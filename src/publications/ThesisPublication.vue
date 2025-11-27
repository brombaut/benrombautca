<template>
  <div class="publication-card">
    <div class="publication-year-badge">{{ thesis.year }}</div>
    <div class="publication-content">
      <h4 class="publication-title">{{ thesis.title }}</h4>
      <div class="publication-meta">
        <span class="publication-authors">{{ thesis.authors }}</span>
        <span class="publication-separator">•</span>
        <span class="publication-type">{{ thesis.thesisType }}</span>
      </div>
      <div class="publication-venue">{{ thesis.venue }}</div>
      <div class="publication-links">
        <a
          v-for="link in thesis.links"
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
import { ThesisPublication } from "./types";

export default defineComponent({
  name: "ThesisPublication",
  props: {
    thesis: {
      type: Object as PropType<ThesisPublication>,
      required: true,
    },
    publicationNumber: {
      type: Number,
      required: true,
    },
  },
});
</script>

<style lang="scss">
</style>
