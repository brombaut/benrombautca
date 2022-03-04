<template>
<li class="journal-publication">
  <div class="publication-index">[{{journal.type}}{{publicationNumber}}]</div>
  <div class="publication-info">
    <div class="publication-info-entity title">
      <span><b>{{ journal.title }}</b></span>
    </div>
    <div class="publication-info-entity authors">
      <span
        v-for="(a, idx) in journal.authors"
        :key=a>
        <span :class="{underline: authorIsBen(a)}">{{ a }}</span>
        <span v-if="idx < journal.authors.length - 1">, </span>
        <span v-else>.</span>
      </span>
    </div>
    <div class="publication-info-entity venue">
      <i>{{ journal.venue }}</i>, {{ journal.year }}
    </div>
  </div>
</li>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { JournalPublication } from "./types";

export default Vue.extend({
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
.journal-publication {
  display: flex;
  flex-direction: row;
}

</style>
