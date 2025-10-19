<template>
  <section id="hikes">
    <SectionHeader
      title="Hiking"
      icon="hiking"
      subtext="Some of the hikes I've done over the years." />
    <div class="section-body">
      <HikingCard
        v-for="hike in orderedHikes"
        :key="new Date(hike.date).getTime()"
        :hike="hike" />
    </div>
  </section>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import HikingCard from "./HikingCard.vue";
import hikes from "./hikes";
import { Hike } from "./types";

export default defineComponent({
  name: "HikingSection",
  components: {
    SectionHeader,
    HikingCard,
  },
  data() {
    return {
      hikes,
    };
  },
  computed: {
    orderedHikes(): Hike[] {
      return this.hikes.sort((a: Hike, b: Hike) => {
        return b.orderDate.getTime() - a.orderDate.getTime();
      });
    }
  }
});
</script>

<style lang="scss">
#hikes {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
