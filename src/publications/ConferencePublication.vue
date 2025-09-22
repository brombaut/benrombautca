<template>
<li class="conference-publication">
  <div class="publication-index">[{{conference.type}}{{publicationNumber}}]</div>
  <div class="publication-info">
    <div class="publication-info-entity title">
      <span><b>{{ conference.title }}</b></span>
    </div>
    <div class="publication-info-entity authors">
      <span
        v-for="(a, idx) in conference.authors"
        :key=a>
        <span :class="{underline: authorIsBen(a)}">{{ a }}</span>
        <span v-if="idx < conference.authors.length - 1">, </span>
        <span v-else>.</span>
      </span>
    </div>
    <div class="publication-info-entity venue">
      <i>{{ conference.conferenceName }}</i>, {{ conference.venue }}, {{ conference.month }} {{ conference.year }}
    </div>
    <div class="links">
      <a
        v-for="link in conference.links"
        :key="link.url"
        :href="link.url"
        target="_blank">
        <span>[{{ link.type }}]</span>
      </a>
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
.conference-publication {
  display: flex;
  flex-direction: row;
}
</style>