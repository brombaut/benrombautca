<template>
  <li class="work-card align-left slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="work.imageFile" />
    </div>
    <div class="title">{{ work.title }}</div>
    <div class="company">
      <font-awesome-icon
        class="icon"
        :icon="['fas', 'building']"
      />
      {{ work.company }}
    </div>
    <div class="time">
      <font-awesome-icon
        class="icon"
        :icon="['fas', 'calendar']"
      />
      {{ work.time }}
    </div>
    <div class="location">
      <font-awesome-icon
        class="icon"
        :icon="['fas', 'map-marker-alt']"
      />
      {{ work.location }}
    </div>
    <!-- <div class="worked-with-list">
      <span>Worked With: </span>
      <span
        v-for="ww in work.workedWith"
        :key="ww"
        class="worked-with">
        {{ ww }}
      </span>
    </div> -->
  </li>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import { Work } from "../types/work";

@Component
export default class WorkCard extends Vue {
  @Prop()
  private work!: Work;

  private workCardElem!: HTMLLIElement;

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
li {
  font-size: 2.5rem;
  color: $primary;
}
.work-card {
  text-align: left;
  padding: 4px 20px;

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
    padding-top: 4px;
  }

  .company {
    font-weight: bold;
  }

  .icon {
    color: $primaryDark;
    margin-right: 4px;
    filter: brightness(85%);
  }

  .worked-with-list {
    display: flex;
    align-items: center;

    .worked-with {
      background: $primaryDark;
      filter: brightness(90%);
      margin: 4px;
      padding: 4px;
      border-radius: 4px;
      text-align: center;
      font-size: 0.8rem;
    }
  }
}
</style>
