<template>
  <section id="publications">
    <!-- subtext="This page contains links to all of my publications." -->
    <SectionHeader
      title="Publications"
      icon="paragraph"
      subtext="This page contains links to my publications." />
    <div class="section-body">
      <div
        v-for="vPub in viewPublications"
        :key="vPub.type">
        <h3 class="publication-type-header">{{ vPub.header }}</h3>
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
          items: this.publications
            .filter((p: Publication) => p.type === t)
            .sort((a: Publication, b: Publication) => b.dateAccepted.getTime() - a.dateAccepted.getTime()),
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
});
</script>

<style lang="scss">
#publications {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    .publication-type-header {
      color: $primaryDark;
    }

    ul {
      padding-inline-start: 8px;
      margin-block-start: 8px;
      margin-block-end: 20px;

      li {
        margin: 8px 0;

          .underline {
            text-decoration: underline;
          }

          .publication-index{
            margin: 6px 16px;
            color: $primaryDark;
          }

          .publication-info-entity {
            margin: 6px 0;
          }

          .title {
            color: $primary;
          }

          .links {
            a {
              font-weight: 500;
              margin-right: 8px;
              color: $primaryDark;

              &:hover {
                cursor: pointer;
              }
            }
          }
      }
    }
  }

}
</style>
