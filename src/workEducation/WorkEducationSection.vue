<template>
  <section id="work-education">
    <VerticalTimeline
      id="work"
      type="work"
      title="Work"
      icon="code"
      :timelineEntities="workEntities"
      :showLimit="4"
    />
    <VerticalTimeline
      id="education"
      v-if="true"
      type="education"
      title="Education"
      icon="graduation-cap"
      :timelineEntities="educationEntities"
    />
  </section>
</template>

<script lang="ts">
import VerticalTimeline from "./VerticalTimeline.vue";
import educationEntities from "./educationEntities";
import workEntities from "./workEntities";

export default {
  name: "WorkEducationSection",
  components: {
    VerticalTimeline,
  },
  data() {
    return {
      educationEntities,
      workEntities,
    };
  },
};
</script>

<style lang="scss">
#work-education {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
}
</style>
