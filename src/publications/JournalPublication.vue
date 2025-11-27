<template>
  <li class="journal-publication">
    <div class="publication-card">
      <div class="publication-year-badge">
        {{ journal.year }}
      </div>
      <div class="publication-content">
        <div class="publication-header">
          <div class="publication-title">{{ journal.title }}</div>
          <div class="publication-type-badge">{{ journal.type }}{{ publicationNumber }}</div>
        </div>
        <div class="publication-authors">
          <span
            v-for="(a, idx) in journal.authors"
            :key="a">
            <span class="author-name" :class="{ 'is-ben': authorIsBen(a) }">{{ a }}</span><span v-if="idx < journal.authors.length - 1">, </span>
          </span>
        </div>
        <div class="publication-venue">
          <span class="venue-name">{{ journal.venue }}</span> • {{ journal.month }} {{ journal.year }}
        </div>
        <div class="publication-links">
          <a
            v-for="link in journal.links"
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
