<template>
  <section id="hikes">
    <SectionHeader
      title="Hiking"
      icon="hiking"
      subtext="I got into hiking as a way to explore nature and stay active. Now I'd like to make a habit of hiking different trails every few years, with some other hikes every now and then. I completed my first official hike in the Spring of 2022, which is listed below. Hopefully I'll add more to this list in the coming years." />
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
