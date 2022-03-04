<template>
<li class="thesis-publication">
  <div class="publication-index">[{{thesis.type}}{{publicationNumber}}]</div>
  <div class="publication-info">
    <div class="publication-info-entity title">
      <span><b>{{ thesis.title }}</b></span>
    </div>
    <div class="publication-info-entity authors">
      <span class="underline">{{ thesis.authors }}</span> - <span>{{ thesis.thesisType }}</span>
    </div>
    <div class="publication-info-entity venue">
      <i>{{ thesis.venue }}</i>, {{ thesis.year }}
    </div>
  </div>
</li>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ThesisPublication } from "./types";

export default Vue.extend({
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
.thesis-publication {
  display: flex;
  flex-direction: row;
}

</style>
