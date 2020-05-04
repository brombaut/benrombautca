<template>
  <li class="education-card align-right slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="education.imageFile" />
    </div>
    <div class="title">{{ education.title }}</div>
    <div class="institution">{{ education.institution }}</div>
    <div class="time">{{ education.time }}</div>
  </li>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { Education } from "../types/education";

@Component
export default class EducationCard extends Vue {
  @Prop()
  private education!: Education;

  private educationCardElem!: HTMLLIElement;

  get imageSource() {
    try {
      if (!this.education.imageFile) {
        return "";
      }
      const images = require.context("../assets/images/", false, /(\.jpg || \.png)$/);
      return images(`./${this.education.imageFile}`);
    } catch (e) {
      return "";
    }
  }

  checkSlide(e: Event) {
    const boundingRect: DOMRect = this.educationCardElem.getBoundingClientRect();
    const { width, height } = boundingRect;
    const slideInAt = (window.scrollY + window.innerHeight - height / 2);
    const imageBottom = this.educationCardElem.offsetTop + height;
    const isHalfShown = slideInAt > this.educationCardElem.offsetTop;
    const isHalfScrolledPast = window.scrollY < imageBottom;
    if (isHalfShown && isHalfScrolledPast) {
      this.educationCardElem.classList.add("active");
      window.removeEventListener("scroll", this.checkSlide);
    }
  }

  mounted() {
    this.educationCardElem = this.$el as HTMLLIElement; // .querySelector(".slide-in") as HTMLLIElement;
    window.addEventListener("scroll", this.checkSlide);
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
    color: white;
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
}
</style>
