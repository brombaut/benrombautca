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
        <i>{{ thesis.venue }}</i>, {{ thesis.month }} {{ thesis.year }}
      </div>
      <div class="publication-info-entity links">
        <a
          v-for="link in thesis.links"
          :key="link.url"
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer">
          <span>[{{ link.type }}]</span>
        </a>
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
.thesis-publication {
  display: flex;
  flex-direction: row;
}

</style>
