<template>
  <section id="races">
    <SectionHeader
      title="Running"
      icon="running"
      subtext="I got into running while the pandemic had the gyms closed. Now I'd like to make a habit of running a different marathon every few years, with some other races every now and then. I ran my first official marathon in the Spring of 2022, which is listed below. Hopefully I'll add more to this list in the coming years." />
    <div class="section-body">
      <RunningCard
        v-for="race in races"
        :key="race.name"
        :race="race" />
    </div>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import RunningCard from "./RunningCard.vue";
import races from "./races";

export default Vue.extend({
  name: "RunningSection",
  components: {
    SectionHeader,
    RunningCard,
  },
  data() {
    return {
      races,
    };
  },
});
</script>

<style lang="scss">
#races {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
