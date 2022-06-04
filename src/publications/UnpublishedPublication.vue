<template>
<li class="unpublished-publication">
  <div class="publication-index">[{{unpublishedPublication.type}}{{publicationNumber}}]</div>
  <div class="publication-info">
    <div class="publication-info-entity title">
      <span><b>{{ unpublishedPublication.title }}</b></span>
    </div>
    <div class="publication-info-entity authors">
      <span
        v-for="(a, idx) in unpublishedPublication.authors"
        :key=a>
        <span :class="{underline: authorIsBen(a)}">{{ a }}</span>
        <span v-if="idx < unpublishedPublication.authors.length - 1">, </span>
        <span v-else>.</span>
      </span>
    </div>
    <div class="links">
      <a
        v-for="link in unpublishedPublication.links"
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
import { UnpublishedPublication } from "./types";

export default Vue.extend({
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
.unpublished-publication {
  display: flex;
  flex-direction: row;
}

</style>
