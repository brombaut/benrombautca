<template>
  <li class="education-card">
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
}
</script>

<style lang="scss">
li {
  font-size: 2.5rem;
  color: $primary;
}
.education-card {
  text-align: left;
  padding: 0px 20px;

  div {
    margin: 4px;
    font-size: 1rem;
    color: white;
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
