<template>
  <section id="about-me">
    <SectionHeader title="About Me" icon="user" />
    <div class="section-body">
      <div class="image-container">
        <SkeletonLoader
          :imagePath="aboutMe.imageFileName"
          imageAlt="Ben Rombaut"
          :isCircle="true" />
      </div>
      <div class="text-container" v-html="aboutMe.description" />
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import aboutMe from "./aboutMe";
import { AboutMe } from "./about-me";
import SectionHeader from "../shared/SectionHeader.vue";
import SkeletonLoader from "../shared/SkeletonLoader.vue";

export default defineComponent({
  name: "AboutMeSection",
  components: {
    SectionHeader,
    SkeletonLoader,
  },
  data() {
    return {
      aboutMe: aboutMe as AboutMe, // B-E-A-U-tiful
    };
  },
});
</script>

<style lang="scss">
#about-me {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin: 8px 0px;

    @media screen and (max-width: $MEDIUM_DISPLAY_SIZE) {
      flex-direction: column;
    }

    .text-container {
      flex: 1;
      p {
        text-align: left;
        font-size: 1.2rem;

        @media screen and (max-width: $SMALL_DISPLAY_SIZE) {
          font-size: 1rem;
        }

        @media screen and (max-width: $PHONE_DISPLAY_SIZE) {
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
    }

    @media only screen and (max-width: $TINY_DISPLAY_SIZE) {
      .image-container {
        height: 200px;
        width: 200px;
        margin: 0;
      }
    }
  }
}
</style>
