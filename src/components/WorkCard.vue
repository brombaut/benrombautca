<template>
  <li class="work-card">
    <div v-if="true || work.imageFile" class="image-container">
      <img :src="imageSource" :alt="work.imageFile" />
    </div>
    <div class="title">{{ work.title }}</div>
    <div class="company-time">
      <span class="company">{{ work.company }}</span>
      <span class="time">{{ work.time }}</span>
    </div>
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
    transform: translateY(-20px);
  }

  .image-container {
    height: 45px;
    margin-bottom: 0px;
    margin-top: 20px;

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
