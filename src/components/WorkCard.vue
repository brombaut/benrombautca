<template>
  <li class="work-card">
    <div v-if="true || work.imageFile" class="image-container">
      <img :src="imageSource" :alt="work.imageFile" />
    </div>
    <div class="title">{{ work.title }}</div>
    <div class="company"><i>{{ work.company }}</i></div>
      <!-- <span class="company">{{ work.company }}</span> -->
      <!-- <span class="time"><i>{{ work.time }}</i></span> -->
    <!-- </div> -->
    <div class="time">{{ work.time }}</div>
    <div class="location">
      {{ work.location }}
    </div>
  </li>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { Work } from "../types/work";

@Component
export default class WorkCard extends Vue {
  @Prop()
  private work!: Work;

  get imageSource() {
    try {
      if (!this.work || !this.work.imageFile) {
        return "";
      }
      const images = require.context("../assets/images/", false, /(\.jpg || \.png)$/);
      return images(`./${this.work.imageFile}`);
    } catch (e) {
      return "";
    }
  }
}
</script>

<style lang="scss">
li {
  font-size: 2.5rem;
  color: $primary;
}
.work-card {
  text-align: left;
  padding: 0px 20px;

  div {
    margin: 4px;
    font-size: 1rem;
    color: white;
    transform: translateY(8px);
  }

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

  .title {
    font-size: 1.2rem;
    font-weight: 800;
    color: $primary;
  }

  .company {}

  .time {
    // margin-left: 4px;
    // font-size: 0.8rem;
    // color: $primaryDark;
  }
}
</style>
