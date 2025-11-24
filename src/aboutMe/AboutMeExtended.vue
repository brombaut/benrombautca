<template>
  <div class="about-me-extended">
    <AboutMeSection />
    <WorkEducationSection />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AboutMeSection from "@/aboutMe/AboutMeSection.vue";
import WorkEducationSection from "@/workEducation/WorkEducationSection.vue";

export default defineComponent({
  name: "AboutMeExtended",
  components: {
    AboutMeSection,
    WorkEducationSection,
  },
});
</script>

<style lang="scss">
.about-me-extended {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
</style>
