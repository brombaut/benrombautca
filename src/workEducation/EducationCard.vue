<template>
  <li class="education-card align-right slide-in">
    <div class="list-item-bullet"></div>
    <div class="list-item-content">
      <div class="list-item-item image-container">
        <img :src="imageSource" :alt="education.imageFile" />
      </div>
      <div class="list-item-item title">{{ education.title }}</div>
      <div class="list-item-item lab" v-if="education.lab">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'vial']" />
        </div>
        <div>{{ education.lab }}</div>
      </div>
      <div class="list-item-item faculty">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'school']" />
        </div>
        <div>{{ education.faculty }}</div>
      </div>
      <div class="list-item-item institution">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'university']" />
        </div>
        <div>{{ education.institution }}</div>
      </div>
      <div class="list-item-item location">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'map-marker-alt']" />
        </div>
        <div>{{ education.location }}</div>
      </div>
      <div class="list-item-item time">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'calendar']" />
        </div>
        <div>{{ education.time }}</div>
      </div>
    </div>
  </li>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import uiUtils from "@/utils/ui-utils";
import { Education } from "./education";

export default Vue.extend({
  name: "EducationCard",
  props: {
    education: {
      type: Object as PropType<Education>,
      required: true,
    },
  },
  computed: {
    imageSource(): any {
      return uiUtils.loadImage(this.education.imageFile);
    },
  },
  methods: {
    localCheckSlide(): void {
      uiUtils.checkSlide(this.$el as HTMLLIElement, this.localCheckSlide);
    },
  },
  mounted(): void {
    window.addEventListener("scroll", this.localCheckSlide);
    this.localCheckSlide();
  },
});
</script>

<style lang="scss">
.education-card {

  .image-container {
    height: 52px;
    margin-bottom: 16px;
    margin-top: 40px;

    img {
      height: 100%;
    }
  }
}
</style>
