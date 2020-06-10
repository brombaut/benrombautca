<template>
  <section id="road-maps-section">
    <SectionHeader title="YEARLY ROADMAPS" icon="map-marked-alt" />
    <div class="section-body">
      <RoadMap
        v-for="roadmap in roadmaps"
        :key="roadmap.year"
        :roadmap="roadmap"
        :openedYear="openedYear"
        @yearClicked="updateYear"
      />
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import RoadMap from "./RoadMap.vue";
import roadmaps from "./roadmaps";
import { YearlyRoadmap } from "./yearly-roadmap";
import SectionHeader from "../shared/SectionHeader.vue";

@Component({
  components: {
    RoadMap,
    SectionHeader
  }
})
export default class RoadMapsSection extends Vue {
  private roadmaps: YearlyRoadmap[] = roadmaps;

  private openedYear = 2020;

  updateYear(year: number) {
    this.openedYear = year;
  }
}
</script>

<style lang="scss">
#road-maps-section {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
