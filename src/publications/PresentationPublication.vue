<template>
  <li class="presentation-publication">
    <div class="publication-card">
      <div class="publication-year-badge">
        {{ presentation.year }}
      </div>
      <div class="publication-content">
        <div class="publication-header">
          <div class="publication-title">{{ presentation.title }}</div>
          <div class="publication-type-badge">{{ presentation.type }}{{ publicationNumber }}</div>
        </div>
        <div class="publication-authors">
          <span
            v-for="(a, idx) in presentation.authors"
            :key="a">
            <span class="author-name" :class="{ 'is-ben': authorIsBen(a) }">{{ a }}</span><span v-if="idx < presentation.authors.length - 1">, </span>
          </span>
        </div>
        <div class="publication-venue">
          <span class="venue-name">{{ presentation.venue }}</span> • {{ presentation.location }} • {{ presentation.month }} {{ presentation.year }}
        </div>
        <div class="publication-links">
          <a
            v-for="link in presentation.links"
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
import { PresentationPublication } from "./types";

export default defineComponent({
  name: "PresentationPublication",
  props: {
    presentation: {
      type: Object as PropType<PresentationPublication>,
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
