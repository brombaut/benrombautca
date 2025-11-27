<template>
  <li class="conference-publication">
    <div class="publication-card">
      <div class="publication-year-badge">
        {{ conference.year }}
      </div>
      <div class="publication-content">
        <div class="publication-header">
          <div class="publication-title">{{ conference.title }}</div>
          <div class="publication-type-badge">{{ conference.type }}{{ publicationNumber }}</div>
        </div>
        <div class="publication-authors">
          <span
            v-for="(a, idx) in conference.authors"
            :key="a">
            <span class="author-name" :class="{ 'is-ben': authorIsBen(a) }">{{ a }}</span><span v-if="idx < conference.authors.length - 1">, </span>
          </span>
        </div>
        <div class="publication-venue">
          <span class="venue-name">{{ conference.conferenceName }}</span> • {{ conference.venue }} • {{ conference.month }} {{ conference.year }}
        </div>
        <div class="publication-links">
          <a
            v-for="link in conference.links"
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
