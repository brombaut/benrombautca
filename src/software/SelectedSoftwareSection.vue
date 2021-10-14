<template>
  <section id="selected-software">
    <SectionHeader :title="selectedSoftware.title" icon="" :subtext="selectedSoftware.description"/>
    <div class="meta-container">
      <div class="tech-used">
        <TechUsedIcon
          v-for="tech in selectedSoftware.techUsed"
          :key="tech._id"
          :tech=tech />
      </div>
      <div class="external-profiles">
        <ExternalRepoIcon
          v-for="repo in selectedSoftware.externalRepos"
          :key="repo._id"
          :externalRepo="repo"
          :verbose="true" />
      </div>
      <div class="dates">
        Created {{ formatDate(selectedSoftware.createdAt) }} • Updated {{ formatDate(selectedSoftware.updatedAt) }}
      </div>
    </div>
    <div class="section-body">
      <GitHubMarkdown :content="selectedSoftware.body" />
    </div>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import GitHubMarkdown from "../shared/GitHubMarkdown.vue";
import TechUsedIcon from "./TechUsedIcon.vue";
import ExternalRepoIcon from "./ExternalRepoIcon.vue";

import { SoftwareArticle, SoftwareArticlesProxy } from "./SoftwareArticlesProxy";

export default Vue.extend({
  name: "SelectedSoftwareSection",
  components: {
    SectionHeader,
    GitHubMarkdown,
    TechUsedIcon,
    ExternalRepoIcon,
  },
  data() {
    return {
      selectedSoftwareId: "",
      selectedSoftware: null as (SoftwareArticle | null),
    };
  },
  methods: {
    loadSelectedArticle(aId: string): SoftwareArticle | null {
      const allSoftwareArticles: SoftwareArticle[] = new SoftwareArticlesProxy().softwareArticles;
      const selectedSoftware: SoftwareArticle | undefined = allSoftwareArticles.find((sa: SoftwareArticle) => sa.id === aId);
      return selectedSoftware || null;
    },
    formatDate(d: Date): string {
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
    },
    backToSoftwares(): void {
      this.$router.push({ name: "software" });
    },
  },
  created() {
    window.scrollTo(0, 0);
    this.selectedSoftwareId = this.$router.currentRoute.params.softwareId;
    this.selectedSoftware = this.loadSelectedArticle(this.selectedSoftwareId);
  },
});
</script>

<style lang="scss">
#selected-software {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  .section-header {
    .section-title {
      line-height: 1.5em;
    }
  }

  .meta-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 8px;

    .tech-used,
    .external-profiles {
      display: flex;
      flex-direction: row;
      align-items: center;
      flex-wrap: wrap;
    }

    .dates,
    .tech-used,
    .external-profiles {
      margin: 6px 0px;
    }

  }

  .section-body {
    text-align: left;
    width: 100%;
  }
}

</style>
