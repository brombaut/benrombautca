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
        :key="vPub.type"
        class="publication-type-section">
        <h3 class="publication-type-header">{{ vPub.header }}</h3>
        <h5 class="publication-type-sub-header">{{ vPub.subHeader }}</h5>
        <div class="publications-grid">
          <template v-if="vPub.type === journal">
            <JournalPublication
              v-for="(publication, idx) in vPub.items"
              :key="publication.title"
              :journal="publication"
              :publicationNumber="vPub.items.length - idx" />
          </template>
          <template v-else-if="vPub.type === thesis">
            <ThesisPublication
              v-for="(publication, idx) in vPub.items"
              :key="publication.title"
              :thesis="publication"
              :publicationNumber="vPub.items.length - idx" />
          </template>
          <template v-else-if="vPub.type === presentation">
            <PresentationPublication
              v-for="(publication, idx) in vPub.items"
              :key="publication.title"
              :presentation="publication"
              :publicationNumber="vPub.items.length - idx" />
          </template>
          <template v-else-if="vPub.type === conference">
            <ConferencePublication
              v-for="(publication, idx) in vPub.items"
              :key="publication.title"
              :conference="publication"
              :publicationNumber="vPub.items.length - idx" />
          </template>
          <template v-else-if="vPub.type === unpublished">
            <UnpublishedPublication
              v-for="(publication, idx) in vPub.items"
              :key="publication.title"
              :unpublishedPublication="publication"
              :publicationNumber="vPub.items.length - idx" />
          </template>
        </div>
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

    .publication-type-section {
      width: 100%;
      margin-bottom: 40px;
    }

    .publication-type-header {
      color: $primaryDark;
      margin-bottom: 8px;
    }

    .publication-type-sub-header {
      margin-bottom: 16px;
      color: $fontColor;
      font-weight: 400;
    }

    .publications-grid {
      display: flex;
      flex-direction: column;
      gap: 20px;
      width: 100%;
    }
  }
}

// Unified card styles for all publication types
.publication-card {
  display: flex;
  flex-direction: row;
  gap: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;

  &:hover {
    border-color: $primary;
    box-shadow: 0 2px 8px rgba(51, 129, 219, 0.1);
  }

  .publication-year-badge {
    flex-shrink: 0;
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, $primary, $primaryDark);
    color: white;
    font-weight: 700;
    font-size: 18px;
    border-radius: 8px;
  }

  .publication-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 0;
  }

  .publication-title {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: $fontColor;
    line-height: 1.4;
  }

  .publication-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #6b7280;
  }

  .publication-authors {
    font-weight: 500;
  }

  .publication-separator {
    color: #d1d5db;
  }

  .publication-type {
    color: #6b7280;
  }

  .publication-venue {
    font-size: 14px;
    color: #6b7280;
    font-style: italic;
  }

  .publication-location {
    font-size: 13px;
    color: #9ca3af;
  }

  .publication-links {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 4px;
  }

  .publication-link {
    font-size: 13px;
    font-weight: 500;
    color: $primary;
    text-decoration: none;
    transition: color 0.2s ease;

    &:hover {
      color: $primaryDark;
      text-decoration: underline;
    }
  }

  @media (max-width: $SMALL_DISPLAY_SIZE) {
    flex-direction: column;
    gap: 16px;

    .publication-year-badge {
      width: 56px;
      height: 56px;
      font-size: 16px;
    }
  }
}
</style>
