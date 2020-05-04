<template>
  <div id="app">
    <MouseTrailer v-if="false"/>
    <LandingSection />
    <AboutMeSection />
    <WorkEducationSection />
    <ProjectsSection />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import LandingSection from "@/components/LandingSection.vue";
import AboutMeSection from "@/components/AboutMeSection.vue";
import ProjectsSection from "@/components/ProjectsSection.vue";
import WorkEducationSection from "@/components/WorkEducationSection.vue";
import MouseTrailer from "@/components/MouseTrailer.vue";

@Component({
  components: {
    LandingSection,
    AboutMeSection,
    ProjectsSection,
    MouseTrailer,
    WorkEducationSection
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
html,
body {
  margin: 0;
  background: $secondary;
}

#app {
  font-family: League Spartan, Helvetica, Arial, sans-serif;
  font-family: "Share Tech Mono", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
  background: $secondary;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  overflow-y: auto;
  overflow-x: auto;
  position: relative;

  section {
    width: calc(100% - 16px);
    max-width: 1280px;
    padding: 48px 8px;
    z-index: 2;
  }
}
</style>
