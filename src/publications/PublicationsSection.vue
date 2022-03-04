<template>
  <section id="articles">
    <SectionHeader
      title="Publications"
      icon="paragraph"
      subtext="This page contains links to all of my publications."/>
    <div class="section-body">
      <div
        v-for="vPub in viewPublications"
        :key="vPub.type">
        <h3>{{ vPub.header }}</h3>
        <ul v-if="vPub.type === journal">
          <JournalPublication
            v-for="(publication, idx) in vPub.items"
            :key="publication.title"
            :journal="publication"
            :publicationNumber="vPub.items.length - idx"/>
        </ul>
        <ul v-else-if="vPub.type === thesis">
          <ThesisPublication
            v-for="(publication, idx) in vPub.items"
            :key="publication.title"
            :thesis="publication"
            :publicationNumber="vPub.items.length - idx"/>
        </ul>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import JournalPublication from "./JournalPublication.vue";
import ThesisPublication from "./ThesisPublication.vue";
import publications from "./publications";
import { Publication, PublicationType, ViewPublication } from "./types";

export default Vue.extend({
  name: "PublicationsSection",
  components: {
    SectionHeader,
    JournalPublication,
    ThesisPublication,
  },
  data() {
    const publicationTypesToShow: PublicationType[] = [
      PublicationType.Journal,
      PublicationType.Thesis,
    ];
    return {
      publicationTypesToShow,
      publications,
    };
  },
  computed: {
    viewPublications(): ViewPublication[] {
      const result = this.publicationTypesToShow.map((t: PublicationType) => {
        return {
          type: t,
          header: this.publicationTypeHeader(t),
          items: this.publications.filter((p: Publication) => p.type === t), // TODO: Sort by date
        };
      });
      return result;
    },
    journal() {
      return PublicationType.Journal;
    },
    thesis() {
      return PublicationType.Thesis;
    },
  },
  methods: {
    publicationTypeHeader(type: PublicationType): string {
      switch (type) {
      case (PublicationType.Journal): return "Peer-reviewed Journal Papers";
      case (PublicationType.Conference): return "Peer-reviewed Conference Papers";
      case (PublicationType.Thesis): return "Theses";
      default: return "";
      }
    },
  },
  mounted() {
    console.log(this.publications);
  },
});
</script>

<style lang="scss">
#articles {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  ul {
    padding-inline-start: 8px;
    margin-block-start: 8px;
    margin-block-end: 20px;

      .underline {
        text-decoration: underline;
      }

      .publication-index,
      .publication-info{
        margin: 4px 4px;
      }
  }

}
</style>
