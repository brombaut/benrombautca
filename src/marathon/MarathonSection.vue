<template>
  <section id="marathon-22">
    <SectionHeader
      title="Marathon '22"
      icon="running"
      subtext="My sister and I are planning to run the Ottawa Marthon in the spring of 2022. Here's my progress."/>
    <div class="section-body">
      <iframe
        height='160'
        width='100%'
        frameborder='0'
        allowtransparency='true'
        scrolling='no'
        referrerpolicy="same-origin"
        sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups allow-pointer-lock allow-popups-to-escape-sandbox"
        src='https://www.strava.com/athletes/55788923/activity-summary/18c7b0585fb6728faa7bc3969530b5f8f1b90dbe' />

      <iframe
        height='454'
        width='100%'
        frameborder='0'
        allowtransparency='true'
        scrolling='no'
        src='https://www.strava.com/athletes/55788923/latest-rides/18c7b0585fb6728faa7bc3969530b5f8f1b90dbe' />

      <!-- <iframe
        height='160'
        width='300'
        frameborder='0'
        allowtransparency='true'
        scrolling='no'
        src='https://www.strava.com/athletes/55788923/activity-summary/18c7b0585fb6728faa7bc3969530b5f8f1b90dbe' /> -->
      <!-- <iframe
        height='454'
        width='300'
        frameborder='0'
        allowtransparency='true'
        scrolling='no'
        src='https://www.strava.com/athletes/55788923/latest-rides/18c7b0585fb6728faa7bc3969530b5f8f1b90dbe' /> -->
    </div>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import Cookies from "js-cookie";
import SectionHeader from "../shared/SectionHeader.vue";

export default Vue.extend({
  name: "MarathonSection",
  components: {
    SectionHeader,
  },
  beforeCreate() {
    Cookies.set("sp", "4f0c95a0-a60a-44e7-be05-e63f13156116", { secure: true, sameSite: "None" });
    Cookies.set("_strava4_session", "4f0c95a0-a60a-44e7-be05-e63f13156116", { secure: true, sameSite: "None" });
  },
});
</script>

<style lang="scss">
#marathon-22 {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
