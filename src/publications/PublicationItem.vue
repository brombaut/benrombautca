<template>
  <li class="publication-item">
    <div class="publication-info">
      <div class="publication-info-entity title">
        <span><b>{{ publication.title }}</b></span>
      </div>
      <div class="publication-info-entity authors">
        <span
          v-for="(a, idx) in publication.authors"
          :key=a>
          <span :class="{ underline: authorIsBen(a) }">{{ a }}</span>
          <span v-if="idx < publication.authors.length - 1">, </span>
        </span>
      </div>
      <div class="publication-info-entity venue">
        <b>{{ publication.venue }}</b>, {{ publication.month }} {{ publication.year }}
      </div>
      <div class="publication-info-entity links">
        <a
          v-for="link in publication.links"
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
import { Publication } from "./types";

export default defineComponent({
  name: "PublicationItem",
  props: {
    publication: {
      type: Object as PropType<Publication>,
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
.publication-item {
  display: flex;
}
</style>
