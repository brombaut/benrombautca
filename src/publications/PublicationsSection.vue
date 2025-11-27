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
            :publicationNumber="vPub.items.length - idx" />
        </ul>
        <ul v-else-if="vPub.type === thesis">
          <ThesisPublication
            v-for="(publication, idx) in vPub.items"
            :key="publication.title"
            :thesis="publication"
            :publicationNumber="vPub.items.length - idx" />
        </ul>
        <ul v-else-if="vPub.type === presentation">
          <PresentationPublication
            v-for="(publication, idx) in vPub.items"
            :key="publication.title"
            :presentation="publication"
            :publicationNumber="vPub.items.length - idx" />
        </ul>
        <ul v-else-if="vPub.type === conference">
          <ConferencePublication
            v-for="(publication, idx) in vPub.items"
            :key="publication.title"
            :conference="publication"
            :publicationNumber="vPub.items.length - idx" />
        </ul>
        <ul v-if="vPub.type === unpublished">
          <UnpublishedPublication
            v-for="(publication, idx) in vPub.items"
            :key="publication.title"
            :unpublishedPublication="publication"
            :publicationNumber="vPub.items.length - idx" />
        </ul>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import JournalPublication from "./JournalPublication.vue";
import ThesisPublication from "./ThesisPublication.vue";
import PresentationPublication from "./PresentationPublication.vue";
import UnpublishedPublication from "./UnpublishedPublication.vue";
import ConferencePublication from "./ConferencePublication.vue";
import publications from "./publications";
import { Publication, PublicationType, ViewPublication } from "./types";

export default defineComponent({
  name: "PublicationsSection",
  components: {
    SectionHeader,
    JournalPublication,
    ThesisPublication,
    PresentationPublication,
    UnpublishedPublication,
    ConferencePublication,
  },
  data() {
    const publicationTypesToShow: PublicationType[] = [
      PublicationType.Conference,
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
            .sort((a: Publication, b: Publication) => (
              b.dateAccepted.getTime() - a.dateAccepted.getTime()
            )),
        };
      });
      return result;
    },
    journal() {
      return PublicationType.Journal;
    },
    conference() {
      return PublicationType.Conference;
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
      case (PublicationType.Journal): return "Journal";
      case (PublicationType.Conference): return "Conference";
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
    width: 100%;

    .publication-type-header {
      color: $primaryDark;
      margin-top: 32px;
      margin-bottom: 8px;
      font-size: 1.5rem;
      border-bottom: 2px solid $primary;
      padding-bottom: 8px;
      width: 100%;
    }

    .publication-type-sub-header {
      margin-bottom: 16px;
      color: $fontColor;
      font-weight: 400;
    }

    ul {
      padding: 0;
      margin: 0;
      list-style: none;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 20px;

      li {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

        &:hover {
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          border-color: $primary;
        }

        .publication-card {
          display: flex;
          gap: 20px;

          .publication-year-badge {
            flex-shrink: 0;
            width: 60px;
            height: 60px;
            background: $primary;
            color: white;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
          }

          .publication-content {
            flex: 1;
            min-width: 0;

            .publication-header {
              display: flex;
              align-items: flex-start;
              justify-content: space-between;
              gap: 12px;
              margin-bottom: 12px;

              .publication-title {
                flex: 1;
                font-size: 1.1rem;
                font-weight: 600;
                color: $primaryDark;
                line-height: 1.4;
              }

              .publication-type-badge {
                flex-shrink: 0;
                background: $secondary;
                color: $primaryDark;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 0.75rem;
                font-weight: 600;
              }
            }

            .publication-authors {
              color: $fontColor;
              font-size: 0.95rem;
              margin-bottom: 8px;
              line-height: 1.5;

              .author-name {
                &.is-ben {
                  font-weight: 600;
                  color: $primary;
                }
              }
            }

            .publication-venue {
              color: #666;
              font-size: 0.9rem;
              margin-bottom: 12px;
              line-height: 1.4;

              .venue-name {
                font-style: italic;
              }
            }

            .publication-links {
              display: flex;
              flex-wrap: wrap;
              gap: 8px;

              a {
                display: inline-flex;
                align-items: center;
                padding: 6px 12px;
                background: $secondary;
                color: $primaryDark;
                border-radius: 4px;
                text-decoration: none;
                font-size: 0.85rem;
                font-weight: 500;
                transition: all 0.2s ease;

                &:hover {
                  background: $primary;
                  color: white;
                }
              }
            }
          }
        }
      }
    }
  }

  @media (max-width: $SMALL_DISPLAY_SIZE) {
    .section-body ul li {
      .publication-card {
        flex-direction: column;
        gap: 12px;

        .publication-year-badge {
          width: 50px;
          height: 50px;
          font-size: 1rem;
        }
      }
    }
  }
}
</style>
