<template>
  <section id="marathons">
    <!-- subtext="This page contains links to all of my publications." -->
    <SectionHeader
      title="Marathons"
      icon="paragraph"
      subtext="This page contains links to my publications." />
    <div class="section-body">
    </div>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import SectionHeader from "../shared/SectionHeader.vue";

export default Vue.extend({
  name: "MarathonsSection",
  components: {
    SectionHeader,
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
