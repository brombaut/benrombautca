<template>
  <li class="work-card align-left slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="work.imageFile" />
    </div>
    <div class="title">{{ work.title }}</div>
    <div class="company">
      <font-awesome-icon class="icon" :icon="['fas', 'building']" />
      <a :href="work.link" target="_blank">{{ work.company }}</a>
    </div>
    <div class="time">
      <font-awesome-icon class="icon" :icon="['fas', 'calendar']" />
      {{ work.time }}
    </div>
    <div class="location">
      <font-awesome-icon class="icon" :icon="['fas', 'map-marker-alt']" />
      {{ work.location }}
    </div>
  </li>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import { Work } from "./work";

@Component
export default class WorkCard extends Vue {
  @Prop()
  private work!: Work;

  private workCardElem!: HTMLLIElement;

  get imageSource() {
    return uiUtils.loadImage(this.work.imageFile);
  }

  localCheckSlide() {
    uiUtils.checkSlide(this.workCardElem, this.localCheckSlide);
  }

  mounted() {
    this.workCardElem = this.$el as HTMLLIElement;
    window.addEventListener("scroll", this.localCheckSlide);
    this.localCheckSlide();
  }
}
</script>

<style lang="scss">
.work-card {

  .image-container {
    height: 45px;
    max-width: 144px;
    margin-bottom: 0px;
    margin-top: 32px;

    img {
      height: 100%;
      width: 100%;
      border-radius: 4px;
    }
  }

  .company {
    font-weight: bold;
  }
}
</style>
