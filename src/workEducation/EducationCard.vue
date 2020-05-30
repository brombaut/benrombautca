<template>
  <li class="education-card align-right slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="education.imageFile" />
    </div>
    <div class="title">{{ education.title }}</div>
    <div class="institution">
      <font-awesome-icon class="icon" :icon="['fas', 'university']" />
      {{ education.institution }}
    </div>
    <div class="time">
      <font-awesome-icon class="icon" :icon="['fas', 'calendar']" />
      {{ education.time }}
    </div>
  </li>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import { Education } from "./education";

@Component
export default class EducationCard extends Vue {
  @Prop()
  private education!: Education;

  private educationCardElem!: HTMLLIElement;

  get imageSource() {
    return uiUtils.loadImage(this.education.imageFile);
  }

  localCheckSlide() {
    uiUtils.checkSlide(this.educationCardElem, this.localCheckSlide);
  }

  mounted() {
    this.educationCardElem = this.$el as HTMLLIElement;
    window.addEventListener("scroll", this.localCheckSlide);
    this.localCheckSlide();
  }
}
</script>

<style lang="scss">
li {
  font-size: 2.5rem;
  color: $primary;
}
.education-card {
  text-align: left;
  padding: 4px 20px;

  div {
    margin: 4px;
    font-size: 1rem;
    transform: translateY(12px);
  }

  .image-container {
    height: 45px;
    width: 40px;
    margin-bottom: 16px;
    margin-top: 40px;

    img {
      height: 100%;
      width: 100%;
    }
  }

  .title {
    font-size: 1.2rem;
    font-weight: 800;
    color: $primary;
  }

  .institution {
    font-weight: bold;
    color: $pFontColor;
  }

  .time {
    color: $pFontColor;
  }

  .icon {
    color: $primaryDark;
    margin-right: 4px;
  }
}
</style>
