<template>
  <div class="publication-item">
    <div class="pub-title">{{ publication.title }}</div>
    <div class="pub-authors">
      <span v-for="(a, idx) in publication.authors" :key="a">
        <span :class="{ 'is-ben': authorIsBen(a) }">{{ a }}</span><span v-if="idx < publication.authors.length - 1">, </span>
      </span>
    </div>
    <div class="pub-meta">
      <span class="pub-venue">{{ publication.venue }}</span>
      <span class="pub-year"> · {{ publication.year }}</span>
    </div>
    <div class="pub-links" v-if="publication.links.length">
      <a
        v-for="link in publication.links"
        :key="link.url"
        :href="link.url"
        target="_blank"
        rel="noopener noreferrer"
        class="pub-link-tag">
        {{ link.type }}
      </a>
    </div>
  </div>
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
  flex-direction: column;
  gap: 4px;
  padding: 20px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);

  &:first-child {
    padding-top: 4px;
  }

  &:last-child {
    border-bottom: none;
  }

  .pub-title {
    font-weight: 600;
    color: $primary;
    font-size: 1.05em;
    line-height: 1.4;
  }

  .pub-authors {
    font-size: 0.9em;
    color: #555;

    .is-ben {
      text-decoration: underline;
    }
  }

  .pub-meta {
    font-size: 0.88em;
    color: #777;

    .pub-venue {
      font-style: italic;
    }
  }

  .pub-links {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 4px;

    .pub-link-tag {
      font-size: 0.8em;
      font-weight: 500;
      color: $primaryDark;
      border: 1px solid $primaryDark;
      border-radius: 3px;
      padding: 1px 7px;
      text-decoration: none;
      transition: background-color 0.15s, color 0.15s;

      &:hover {
        background-color: $primaryDark;
        color: white;
      }
    }
  }
}
</style>
