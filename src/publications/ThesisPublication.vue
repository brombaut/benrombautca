<template>
  <li class="thesis-publication">
    <div class="publication-card">
      <div class="publication-year-badge">
        {{ thesis.year }}
      </div>
      <div class="publication-content">
        <div class="publication-header">
          <div class="publication-title">{{ thesis.title }}</div>
          <div class="publication-type-badge">{{ thesis.type }}{{ publicationNumber }}</div>
        </div>
        <div class="publication-authors">
          <span class="author-name is-ben">{{ thesis.authors }}</span> • {{ thesis.thesisType }}
        </div>
        <div class="publication-venue">
          <span class="venue-name">{{ thesis.venue }}</span> • {{ thesis.month }} {{ thesis.year }}
        </div>
        <div class="publication-links">
          <a
            v-for="link in thesis.links"
            :key="link.url"
            :href="link.url"
            target="_blank"
            rel="noopener noreferrer">
            {{ link.type }}
          </a>
        </div>
      </div>
    </div>
  </li>
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
  methods: {
    authorIsBen(a: string) {
      return a === "Benjamin Rombaut";
    },
  },
});
</script>

<style lang="scss">
// Styles are handled in PublicationsSection.vue
</style>
