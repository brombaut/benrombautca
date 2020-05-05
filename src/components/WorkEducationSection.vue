<template>
  <section id="work-education">
    <VerticalTimeline
      type="work"
      title="WORK"
      icon="briefcase"
      :timelineEntities="workEntities"
      :showLimit="3" />
    <VerticalTimeline
      v-if="true"
      type="education"
      title="EDUCATION"
      icon="graduation-cap"
      :timelineEntities="educationEntities" />
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import VerticalTimeline from "@/components/VerticalTimeline.vue";
import educationEntities from "@/data/educationEntities";
import workEntities from "@/data/workEntities";
import { Education } from "../types/education";
import { Work } from "../types/work";

@Component({
  components: {
    VerticalTimeline
  }
})
export default class WorkEducationSection extends Vue {
  private educationEntities: Education[] = educationEntities;

  private workEntities: Work[] = workEntities;
}
</script>

<style lang="scss">
#work-education {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
}
</style>
