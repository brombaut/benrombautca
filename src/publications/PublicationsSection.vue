<template>
  <section id="publications">
    <!-- subtext="This page contains links to all of my publications." -->
    <SectionHeader
      title="Publications"
      icon="paragraph"
      subtext="This page contains links to publications and presentations to which I've contributed." />
    <div class="section-body">
      <div
        v-for="vPub in viewPublications"
        :key="vPub.type">
        <h3 class="publication-type-header">{{ vPub.header }}</h3>
        <h5 class="publication-type-sub-header">{{ vPub.subHeader }}</h5>
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
        <ul v-else-if="vPub.type === presentation">
          <PresentationPublication
            v-for="(publication, idx) in vPub.items"
            :key="publication.title"
            :presentation="publication"
            :publicationNumber="vPub.items.length - idx"/>
        </ul>
        <ul v-if="vPub.type === unpublished">
          <UnpublishedPublication
            v-for="(publication, idx) in vPub.items"
            :key="publication.title"
            :unpublishedPublication="publication"
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
import PresentationPublication from "./PresentationPublication.vue";
import UnpublishedPublication from "./UnpublishedPublication.vue";
import publications from "./publications";
import { Publication, PublicationType, ViewPublication } from "./types";

export default Vue.extend({
  name: "PublicationsSection",
  components: {
    SectionHeader,
    JournalPublication,
    ThesisPublication,
    PresentationPublication,
    UnpublishedPublication,
  },
  data() {
    const publicationTypesToShow: PublicationType[] = [
      PublicationType.Journal,
      PublicationType.Presentation,
      PublicationType.Thesis,
      PublicationType.Unpublished,
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
          subHeader: this.publicationTypeSubHeader(t),
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
    presentation() {
      return PublicationType.Presentation;
    },
    unpublished() {
      return PublicationType.Unpublished;
    },
  },
  methods: {
    publicationTypeHeader(type: PublicationType): string {
      switch (type) {
      case (PublicationType.Journal): return "Peer-reviewed Journal Articles";
      case (PublicationType.Conference): return "Peer-reviewed Conference Articles";
      case (PublicationType.Thesis): return "Theses";
      case (PublicationType.Presentation): return "Presentations & Talks";
      case (PublicationType.Unpublished): return "Unpublished Works";
      default: return "";
      }
    },
    publicationTypeSubHeader(type: PublicationType): string {
      switch (type) {
      case (PublicationType.Journal): return "";
      case (PublicationType.Conference): return "";
      case (PublicationType.Thesis): return "";
      case (PublicationType.Presentation): return "";
      case (PublicationType.Unpublished): return "The following works have not appeared anywhere, but I list them here for completeness.";
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
