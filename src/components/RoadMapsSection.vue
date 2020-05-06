<template>
  <section id="road-maps-section">
    <div class="section-header">
      <font-awesome-icon :icon="['fas', 'map-marked-alt']" />
      <h4 class="section-title">YEALY ROADMAP</h4>
    </div>
    <div class="section-body">
      <RoadMap
        v-for="roadmap in roadmaps"
        :key="roadmap.year"
        :roadmap="roadmap"
        :openedYear="openedYear"
        @yearClicked="updateYear"/>
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import RoadMap from "@/components/RoadMap.vue";
import roadmaps from "@/data/roadmaps";
import { YearlyRoadmap } from "../types/yearly-roadmap";

@Component({
  components: {
    RoadMap
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

  &:hover {
    .section-header {
      color: $primary;
    }
  }

  .section-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    transition: 0.3s color;

    .section-title {
      margin: 0 8px;
      font-size: 1.2rem;
    }
  }

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
