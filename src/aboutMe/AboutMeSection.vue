<template>
  <section id="about-me">
    <SectionHeader title="About Me" icon="user" />
    <div class="section-body">
      <div class="image-container">
        <img :src="imageSource" alt="Ben Rombaut" />
      </div>
      <div class="text-container" v-html="aboutMe.description">
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

  get imageSource() {
    return uiUtils.loadImage(this.aboutMe.imageFileName);
  }

}
</script>

<style lang="scss">
#about-me {
  display: flex;
  flex-direction: column;

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
        font-size: 1.2rem;

        @media screen and (max-width: 600px) {
          font-size: 1rem;
        }

        @media screen and (max-width: 300px) {
          font-size: 0.8rem;
        }
      }
    }

    .image-container {
      height: 300px;
      width: 300px;
      border: 2px solid $primaryDark;
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
