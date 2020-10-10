<template>
  <div class="about-me-extended">
    <AboutMeSection />
    <WorkEducationSection />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import LandingSection from "@/landing/LandingSection.vue";
import AboutMeSection from "@/aboutMe/AboutMeSection.vue";
import WorkEducationSection from "@/workEducation/WorkEducationSection.vue";

@Component({
  components: {
    LandingSection,
    AboutMeSection,
    WorkEducationSection,
  },
})
export default class AboutMeExtended extends Vue {}
</script>

<style lang="scss">
.about-me-extended {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
</style>
