<template>
  <section id="projects">
    <div class="section-header">
      <font-awesome-icon :icon="['fas', 'folder-open']" />
      <h4 class="section-title">PROJECTS</h4>
    </div>
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

@Component({
  components: {
    ProjectCard
  }
})
export default class ProjectsSection extends Vue {
  private projects: Project[] = projects;
}
</script>

<style lang="scss">
#projects {
  display: flex;
  flex-direction: column;

  &:hover {
    .section-header {
      color: $primary;
    }
  }

  .section-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    transition: 0.3s color;

    .section-title {
      margin: 0 8px;
      font-size: 1.2rem;
    }
  }

  .section-body {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}
</style>
