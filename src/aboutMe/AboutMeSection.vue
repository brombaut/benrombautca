<template>
  <section id="about-me">
    <SectionHeader title="ABOUT ME" icon="user" />
    <div class="section-body">
      <div class="image-container align-left slide-in">
        <img :src="imageSource" alt="Ben Rombaut" />
      </div>
      <div class="text-container">
        <p v-for="obj in aboutMe.description" :key="obj.section">{{ obj.paragraph }}</p>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import aboutMe from "./aboutMe";
import { AboutMe } from "./about-me";
import SectionHeader from "../shared/SectionHeader.vue";

@Component({
  components: {
    SectionHeader,
  },
})
export default class AboutMeSection extends Vue {
  private aboutMe: AboutMe = aboutMe;

  private sliderImage!: HTMLDivElement;

  get imageSource() {
    return uiUtils.loadImage(this.aboutMe.imageFileName);
  }

  localCheckSlide() {
    uiUtils.checkSlide(this.sliderImage, this.localCheckSlide);
  }

  mounted() {
    this.sliderImage = this.$el.querySelector(".slide-in") as HTMLDivElement;
    window.addEventListener("scroll", this.localCheckSlide);
    this.localCheckSlide();
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

    @media only screen and (max-width: 500px) {
      .image-container {
        height: 200px;
        width: 200px;
        margin: 0;
      }
    }
  }
}
</style>
