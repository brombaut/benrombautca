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
        :key="vPub.header">
        <h3 class="publication-type-header">{{ vPub.header }}</h3>
        <h5 class="publication-type-sub-header">{{ vPub.subHeader }}</h5>
        <ul>
          <PublicationItem
            v-for="publication in vPub.items"
            :key="publication.title"
            :publication="publication" />
        </ul>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import PublicationItem from "./PublicationItem.vue";
import publications from "./publications";
import { Publication, ViewPublication } from "./types";

export default defineComponent({
  name: "PublicationsSection",
  components: {
    SectionHeader,
    PublicationItem,
  },
  data() {
    return {
      publications,
    };
  },
  computed: {
    publishedWorks(): Publication[] {
      return this.publications
        .filter((p: Publication) => p.venue !== "Unpublished")
        .sort((a: Publication, b: Publication) => (
          b.dateAccepted.getTime() - a.dateAccepted.getTime()
        ));
    },
    unpublishedWorks(): Publication[] {
      return this.publications
        .filter((p: Publication) => p.venue === "Unpublished")
        .sort((a: Publication, b: Publication) => (
          b.dateAccepted.getTime() - a.dateAccepted.getTime()
        ));
    },
    viewPublications(): ViewPublication[] {
      const result: ViewPublication[] = [];

      // Add published works as a single group
      if (this.publishedWorks.length > 0) {
        result.push({
          type: null as any,
          header: "Publications",
          subHeader: "",
          items: this.publishedWorks,
        });
      }

      // Add unpublished works as a separate group
      if (this.unpublishedWorks.length > 0) {
        result.push({
          type: null as any,
          header: "Unpublished Works",
          subHeader: "The following works have not appeared anywhere, but I list them here for completeness.",
          items: this.unpublishedWorks,
        });
      }

      return result;
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
        margin: 16px 0;

          .publication-info {
            display: flex;
            flex-direction: column;
          }

          .underline {
            text-decoration: underline;
          }

          .publication-info-entity {
            margin: 4px 0;
          }

          .title {
            color: $primary;
            font-size: 1.3em;
            margin-bottom: 8px;
          }

          .authors, .venue, .location, .links {
            margin-left: 20px;
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
