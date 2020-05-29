<template>
  <div id="app">
    <MouseTrailer v-if="showMouseTrailer" />
    <LandingSection :mouseTrailerVisible="showMouseTrailer" @headerClicked="toggleMouseTrailer" />
    <AboutMeSection />
    <WorkEducationSection />
    <ProjectsSection />
    <RoadMapsSection />
    <BookshelfSection />
    <SiteFooter />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import LandingSection from "@/landing/LandingSection.vue";
import AboutMeSection from "@/aboutMe/AboutMeSection.vue";
import ProjectsSection from "@/projects/ProjectsSection.vue";
import WorkEducationSection from "@/workEducation/WorkEducationSection.vue";
import RoadMapsSection from "@/roadmaps/RoadMapsSection.vue";
import MouseTrailer from "@/mouseTrailer/MouseTrailer.vue";
import SiteFooter from "@/footer/SiteFooter.vue";
import BookshelfSection from "@/bookshelf/components/BookshelfSection.vue";

@Component({
  components: {
    LandingSection,
    AboutMeSection,
    ProjectsSection,
    MouseTrailer,
    WorkEducationSection,
    RoadMapsSection,
    SiteFooter,
    BookshelfSection
  }
})
export default class App extends Vue {
  private showMouseTrailer = false;

  toggleMouseTrailer() {
    this.showMouseTrailer = !this.showMouseTrailer;
  }
}
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

  // footer {
  //   z-index: 2;
  // }
}
</style>
