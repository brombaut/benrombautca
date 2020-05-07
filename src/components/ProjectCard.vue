<template>
  <div class="project-card slide-in">
    <a
      :href="projectCardHref"
      class="image-container"
      @click.stop.prevent="handleProjectUrlClick()">
      <img
        v-if="imageSource"
        :src="imageSource"
        :alt="project.name" />
      <div
        v-else
        class="project-acronym">
        {{ project.acronym }}
      </div>
    </a>
    <h4 class="title">{{ project.name }}</h4>
    <p class="description">{{ project.description }}</p>
    <h6
      v-if="project.techUsed.length > 0"
      class="tech-used-title">
      Tech Used
    </h6>
    <div
      v-if="project.techUsed.length > 0"
      class="tech-used">
      <span
        v-for="tech in project.techUsed"
        :key="tech">
        {{ tech }}
      </span>
    </div>
    <div class="links">
      <a
        v-if="project.url"
        :href="project.url">
        <font-awesome-icon
          @click.stop.prevent="handleProjectUrlClick()"
          :icon="['fas', 'external-link-alt']"
        />
      </a>
      <a
        v-if="project.sourceUrl"
        :href="project.sourceUrl">
        <font-awesome-icon
          @click.stop.prevent="handleSourceIconClick()"
          :icon="['fas', 'code']"
        />
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import { Project } from "../types/project";

@Component
export default class ProjectCard extends Vue {
  @Prop()
  project!: Project;

  private projectCardElem!: HTMLDivElement;

  get imageSource() {
    return uiUtils.loadImage(this.project.thumbnail);
  }

  get projectCardHref() {
    return this.project.url ? this.project.url : this.project.sourceUrl;
  }

  handleProjectUrlClick() {
    const url = this.projectCardHref;
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

  localCheckHorizontalFadeIn() {
    uiUtils.checkHorizontalFadeIn(this.projectCardElem, this.localCheckHorizontalFadeIn);
  }

  mounted() {
    this.projectCardElem = this.$el as HTMLDivElement;
    window.addEventListener("scroll", this.localCheckHorizontalFadeIn);
    this.localCheckHorizontalFadeIn();
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

    .project-acronym {
      height: 100%;
      width: 100%;
      border-radius: 12px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: $primaryDarkest;
      font-size: 4rem;
      font-weight: 900;
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
