<template>
  <li class="work-card align-left slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="work.imageFile" />
    </div>
    <div class="title">{{ work.title }}</div>
    <div class="company"><i>{{ work.company }}</i></div>
    <div class="time">{{ work.time }}</div>
    <div class="location">
      {{ work.location }}
    </div>
    <div class="worked-with-list">
      <span>Worked With: </span>
      <span
        v-for="ww in work.workedWith"
        :key="ww"
        class="worked-with">
        {{ ww }}
      </span>
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

  checkSlide(e: Event) {
    const boundingRect: DOMRect = this.workCardElem.getBoundingClientRect();
    const { width, height } = boundingRect;
    const slideInAt = (window.scrollY + window.innerHeight - height / 2);
    const imageBottom = this.workCardElem.offsetTop + height;
    const isHalfShown = slideInAt > this.workCardElem.offsetTop;
    const isHalfScrolledPast = window.scrollY < imageBottom;
    if (isHalfShown && isHalfScrolledPast) {
      this.workCardElem.classList.add("active");
      window.removeEventListener("scroll", this.checkSlide);
    }
  }

  mounted() {
    this.workCardElem = this.$el as HTMLLIElement; // .querySelector(".slide-in") as HTMLLIElement;
    window.addEventListener("scroll", this.checkSlide);
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

  .worked-with-list {
    display: flex;
    align-items: center;

    .worked-with {
      background: $primaryDark;
      filter: brightness(85%);
      margin: 4px;
      padding: 4px;
      border-radius: 4px;
      text-align: center;
      font-size: 0.8rem;
    }
  }
}
</style>
