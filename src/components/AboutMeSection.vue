<template>
  <section id="about-me">
    <div class="section-header">
      <font-awesome-icon :icon="['fas', 'user']" />
      <h4 class="section-title">ABOUT ME</h4>
    </div>
    <div class="section-body">
      <div class="image-container align-left slide-in">
        <img :src="imageSource" alt="Ben Rombaut"/>
      </div>
      <div class="text-container">
        <p v-for="obj in aboutMe.description" :key="obj.section">{{ obj.paragraph }}</p>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import aboutMe from "@/data/aboutMe";
import { AboutMe } from "../types/about-me";

@Component
export default class AboutMeSection extends Vue {
  private aboutMe: AboutMe = aboutMe;

  private sliderImage!: HTMLDivElement;

  get imageSource() {
    if (!this.aboutMe.imageFileName) {
      return "";
    }
    const images = require.context("../assets/images/", false, /(\.jpg || \.png)$/);
    return images(`./${this.aboutMe.imageFileName}`);
  }

  checkSlide(e: Event) {
    const boundingRect: DOMRect = this.sliderImage.getBoundingClientRect();
    const { width, height } = boundingRect;
    const slideInAt = (window.scrollY + window.innerHeight - height / 2);
    const imageBottom = this.sliderImage.offsetTop + height;
    const isHalfShown = slideInAt > this.sliderImage.offsetTop;
    const isHalfScrolledPast = window.scrollY < imageBottom;
    if (isHalfShown && isHalfScrolledPast) {
      this.sliderImage.classList.add("active");
    } else {
      // this.sliderImage.classList.remove("active");
    }
  }

  mounted() {
    this.sliderImage = document.querySelector(".slide-in") as HTMLDivElement;
    window.addEventListener("scroll", this.checkSlide);
  }
}
</script>

<style lang="scss">
#about-me {
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
    align-items: center;

    @media screen and (max-width: 900px) {
      flex-direction: column;
    }

    .text-container {
      flex: 1;
      p {
        text-align: left;
        color: white;
        font-size: 20px;
      }
    }

    .image-container {
      height: 300px;
      width: 300px;
      border: 2px solid $primaryDark;
      animation: borderColorChange $pulseAnimationTime infinite;
      border-radius: 50%;
      margin: 0 32px;

      img {
        height: 100%;
        width: 100%;
        border-radius: 50%;
      }
    }
  }

  .align-left {
    float: left;
    margin-right: 20px;
  }
  .align-right {
    float: right;
    margin-left: 20px;
  }
  .slide-in {
    opacity: 0;
    transition: all .5s;
  }
  .align-left.slide-in {
    transform: translateX(-30%) scale(0.95);
  }

  .align-right.slide-in {
    transform: translateX(30%) scale(0.95);
  }
  .slide-in.active {
    opacity: 1;
    transform: translateX(0%) scale(1);
  }
}
</style>
