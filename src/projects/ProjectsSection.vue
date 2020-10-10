<template>
  <section id="projects">
    <SectionHeader title="PROJECTS" icon="folder-open" />
    <div class="section-body">
      <ProjectCard v-for="project in projects" :key="project.id" :project="project" />
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import projects from "./projects";
import ProjectCard from "./ProjectCard.vue";
import { Project } from "./project";
import SectionHeader from "../shared/SectionHeader.vue";

@Component({
  components: {
    ProjectCard,
    SectionHeader,
  },
})
export default class ProjectsSection extends Vue {
  private projects: Project[] = projects;
}
</script>

<style lang="scss">
#projects {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}
</style>
