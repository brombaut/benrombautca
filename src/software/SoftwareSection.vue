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
import {defineComponent} from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import SoftwareCard from "./SoftwareCard.vue";
import { SoftwareArticle, SoftwareArticlesProxy } from "./SoftwareArticlesProxy";

export default defineComponent({
  name: "SoftwareSection",
  components: {
    SectionHeader,
    SoftwareCard,
  },
  data() {
    return {
      softwareArticles: [] as SoftwareArticle[],
      selectedSoftware: null as (SoftwareArticle | null),
    };
  },
  computed: {
    softwareProjectsToDisplay(): SoftwareArticle[] {
      return this.softwareArticles
        .filter((aa: SoftwareArticle) => aa.show)
        .sort((a: SoftwareArticle, b: SoftwareArticle) => {
          return a.order - b.order;
        });
    },
  },
  methods: {
    softwareClicked(software: SoftwareArticle): void {
      
      this.$router.push({ name: "selectedSoftware", params: { softwareId: software.id } });
      this.selectedSoftware = software;
    },
  },
  created(): void {
    this.softwareArticles = new SoftwareArticlesProxy().softwareArticles;
  },
});
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
