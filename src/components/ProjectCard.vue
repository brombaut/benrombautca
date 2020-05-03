<template>
  <div class="project-card">
    <div class="image-container">
      <img
        :src="imageSource"
        @click.stop.prevent="handleProjectUrlClick()" />
    </div>
    <h4 class="title">{{ project.name }}</h4>
    <p class="description">{{ project.description }}</p>
    <h6 class="tech-used-title">Tech Used</h6>
    <div class="tech-used">
      <span v-for="tech in project.techUsed" :key="tech">{{ tech }}</span>
    </div>
    <div class="links">
      <a :href="project.url">
        <font-awesome-icon
          @click.stop.prevent="handleProjectUrlClick()"
          :icon="['fas', 'external-link-alt']"
        />
      </a>
      <a :href="project.sourceUrl">
        <font-awesome-icon @click.stop.prevent="handleSourceIconClick()" :icon="['fas', 'code']" />
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { Project } from "../types/project";

@Component
export default class ProjectCard extends Vue {
  @Prop()
  project!: Project;

  get imageSource() {
    if (!this.project.thumbnail) {
      return "";
    }
    const images = require.context("../assets/images/", false, /\.png$/);
    return images(`./${this.project.thumbnail}`);
  }

  handleProjectUrlClick() {
    const url = this.project.url ? this.project.url : this.project.sourceUrl;
    if (url) {
      const result: Window | null = window.open(url, "_blank");
      if (result) {
        result.focus();
      }
    }
  }

  handleSourceIconClick() {
    if (!this.project.sourceUrl) {
      return;
    }
    const result: Window | null = window.open(this.project.sourceUrl, "_blank");
    if (result) {
      result.focus();
    }
  }
}
</script>

<style lang="scss">
.project-card {
  width: 340px;
  max-width: calc(100vw - 56px);
  margin: 28px;
  display: flex;
  flex-direction: column;
  text-align: left;

  .image-container {
    height: 192px;
    width: 340px;
    max-width: calc(100vw - 56px);
    border-radius: 12px;
    transition: 0.3s filter;

    img {
      height: 100%;
      width: 100%;
      border-radius: 12px;
    }

    &:hover {
      cursor: pointer;
      filter: brightness(80%);
    }
  }

  .title {
    font-size: 1.2rem;
    margin-bottom: 0;
    color: $primary;
  }

  .description {
    min-height: 60px;
  }

  .tech-used-title {
    margin: 0;
    margin-bottom: 4px;
    font-size: 1rem;
    color: $primary;
  }

  .tech-used {
    span {
      margin: 0 4px;
      font-size: 0.8rem;
    }
  }

  .links {
    display: flex;
    justify-content: flex-start;
    margin: 16px 0;
    transition: color 0.3s;

    a {
      margin-right: 16px;
      font-size: 1rem;
      transition: color 0.3s;
      color: $primaryDark;

      svg {
        color: $primaryDark;
      }

      &:hover {
        color: $primary;
      }

      &:visited {
        color: inherit;
        svg {
          color: inherit;
        }
      }
    }
  }
}
</style>
