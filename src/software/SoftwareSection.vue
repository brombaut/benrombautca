<template>
  <section id="software">
    <SectionHeader
      title="Software"
      icon="code"
      subtext="Software projects I've been working on."/>
    <div class="section-body">
      <div class="software-list">
        <SoftwareCard
          v-for="software in softwareProjectsToDisplay"
          :key="software.id"
          :software="software"
          @clicked="softwareClicked" />
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import SectionHeader from "../shared/SectionHeader.vue";
import SoftwareCard from "./SoftwareCard.vue";
import { SoftwareArticle, SoftwareArticlesProxy } from "./SoftwareArticlesProxy";

@Component({
  components: {
    SectionHeader,
    SoftwareCard,
  },
})
export default class SoftwareSection extends Vue {
  softwareArticles: SoftwareArticle[];
  selectedSoftware: SoftwareArticle | null;

  constructor() {
    super();
    this.softwareArticles = new SoftwareArticlesProxy().softwareArticles;
    this.selectedSoftware = null;
  }

  get softwareProjectsToDisplay(): SoftwareArticle[] {
    return this.softwareArticles
      .filter((aa: SoftwareArticle) => aa.show)
      .sort((a: SoftwareArticle, b: SoftwareArticle) => {
        return b.createdAt.getTime() - a.createdAt.getTime();
      });
  }

  softwareClicked(software: SoftwareArticle) {
    this.$router.push({ name: "selectedSoftware", params: { softwareId: software.id } });
    this.selectedSoftware = software;
  }
}
</script>

<style lang="scss">
#software {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: row;
    align-items: center;

    .software-list {
      display: flex;
      flex-direction: column;
      text-align: left;
    }
  }
}
</style>
