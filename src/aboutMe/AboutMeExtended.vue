<template>
  <div class="about-me-extended">
    <AboutMeSection />
    <WorkEducationSection />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { bus } from "@/main";
import AboutMeSection from "@/aboutMe/AboutMeSection.vue";
import WorkEducationSection from "@/workEducation/WorkEducationSection.vue";

@Component({
  components: {
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
