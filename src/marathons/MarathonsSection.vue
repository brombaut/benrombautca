<template>
  <section id="marathons">
    <SectionHeader
      title="Marathons"
      icon="running"
      subtext="I got into running while the pandemic had all the gyms closed. Now I'd like to make a habit of running a (hopefully different) marathon every 1 or 2 years. " />
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
