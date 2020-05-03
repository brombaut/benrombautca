<template>
  <div id="app">
    <LandingSection />
    <AboutMeSection />
    <ProjectsSection />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import LandingSection from "@/components/LandingSection.vue";
import AboutMeSection from "@/components/AboutMeSection.vue";
import ProjectsSection from "@/components/ProjectsSection.vue";

@Component({
  components: {
    LandingSection,
    AboutMeSection,
    ProjectsSection
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
html,
body {
  margin: 0;
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

  section {
    width: calc(100% - 16px);
    max-width: 1280px;
    padding: 48px 8px;
  }
}
</style>
