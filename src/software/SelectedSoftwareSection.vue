<template>
  <section id="selected-software">
    <SectionHeader :title="selectedSoftware.title" icon="" :subtext="selectedSoftware.description"/>
    <div class="meta-container">
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
import { Component, Vue } from "vue-property-decorator";
import SectionHeader from "../shared/SectionHeader.vue";
import Tag from "../shared/Tag.vue";
import GitHubMarkdown from "../shared/GitHubMarkdown.vue";
import { SoftwareArticle, SoftwareArticlesProxy } from "./SoftwareArticlesProxy";

@Component({
  components: {
    SectionHeader,
    Tag,
    GitHubMarkdown,
  },
})
export default class SelectedSoftwareSection extends Vue {
  selectedSoftwareId: string;
  selectedSoftware: SoftwareArticle | null;

  constructor() {
    super();
    window.scrollTo(0, 0);
    this.selectedSoftwareId = this.$router.currentRoute.params.softwareId;
    this.selectedSoftware = this.loadSelectedArticle(this.selectedSoftwareId);

  }

  loadSelectedArticle(aId: string): SoftwareArticle | null {
    const allSoftwareArticles: SoftwareArticle[] = new SoftwareArticlesProxy().softwareArticles;
    const selectedSoftware: SoftwareArticle | undefined = allSoftwareArticles.find((sa: SoftwareArticle) => sa.id === aId);
    return selectedSoftware || null;
  }

  formatDate(d: Date) {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  }

  backToSoftwares() {
    this.$router.push({ name: "software" });
  }
}
</script>

<style lang="scss">
#selected-software {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  .section-header {
    margin-bottom: 4px;

    .section-title {
      line-height: 1.5em;
    }
  }

  .meta-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 16px;

    .dates {
      margin: 0px 0;
    }

  }

  .section-body {
    text-align: left;
    width: 100%;
  }
}

</style>
