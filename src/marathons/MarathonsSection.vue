<template>
  <section id="marathons">
    <SectionHeader
      title="Marathons"
      icon="running"
      subtext="I got into running while the pandemic had the gyms closed. Now I'd like to make a habit of running a different marathon every few years. I ran my first official marathon in the Spring of 2022, which is listed below. Hopefully I'll add more to this list in the coming years." />
    <div class="section-body">
      <MarathonCard
        v-for="marathon in marathons"
        :key="marathon.name"
        :marathon="marathon" />
    </div>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import MarathonCard from "./MarathonCard.vue";
import marathons from "./marathons";

export default Vue.extend({
  name: "MarathonsSection",
  components: {
    SectionHeader,
    MarathonCard,
  },
  data() {
    return {
      marathons,
    };
  },
});
</script>

<style lang="scss">
#marathons {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
