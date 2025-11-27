<template>
  <li class="unpublished-publication">
    <div class="publication-card">
      <div class="publication-year-badge">
        {{ unpublishedPublication.year }}
      </div>
      <div class="publication-content">
        <div class="publication-header">
          <div class="publication-title">{{ unpublishedPublication.title }}</div>
          <div class="publication-type-badge">{{ unpublishedPublication.type }}{{ publicationNumber }}</div>
        </div>
        <div class="publication-authors">
          <span
            v-for="(a, idx) in unpublishedPublication.authors"
            :key="a">
            <span class="author-name" :class="{ 'is-ben': authorIsBen(a) }">{{ a }}</span><span v-if="idx < unpublishedPublication.authors.length - 1">, </span>
          </span>
        </div>
        <div class="publication-venue">
          <span class="venue-name">{{ unpublishedPublication.venue }}</span> • {{ unpublishedPublication.month }} {{ unpublishedPublication.year }}
        </div>
        <div class="publication-links">
          <a
            v-for="link in unpublishedPublication.links"
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
// Styles are handled in PublicationsSection.vue
</style>
