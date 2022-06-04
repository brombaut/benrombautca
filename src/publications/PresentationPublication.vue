<template>
<li class="presentation-publication">
  <div class="publication-index">[{{presentation.type}}{{publicationNumber}}]</div>
  <div class="publication-info">
    <div class="publication-info-entity title">
      <span><b>{{ presentation.title }}</b></span>
    </div>
    <div class="publication-info-entity authors">
      <span
        v-for="(a, idx) in presentation.authors"
        :key=a>
        <span :class="{underline: authorIsBen(a)}">{{ a }}</span>
        <span v-if="idx < presentation.authors.length - 1">, </span>
        <span v-else>.</span>
      </span>
    </div>
    <div class="publication-info-entity venue">
      <i>{{ presentation.venue }}</i>, {{ presentation.month }} {{ presentation.year }}
    </div>
    <div class="publication-info-entity venue">
      <span>{{ presentation.location }}</span>
    </div>
    <div class="links">
      <a
        v-for="link in presentation.links"
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
import Vue, { PropType } from "vue";
import { PresentationPublication } from "./types";

export default Vue.extend({
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
.presentation-publication {
  display: flex;
  flex-direction: row;
}

</style>
