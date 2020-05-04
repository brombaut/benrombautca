<template>
  <section id="work-education">
    <VerticalTimeline />
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import VerticalTimeline from "@/components/VerticalTimeline.vue";

@Component({
  components: {
    VerticalTimeline
  }
})
export default class WorkEducationSection extends Vue {

}
</script>

<style lang="scss">
#work-education {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  flex-wrap: wrap;
}
</style>
