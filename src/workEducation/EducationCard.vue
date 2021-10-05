<template>
  <li class="education-card align-right slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="education.imageFile" />
    </div>
    <div class="title">{{ education.title }}</div>
    <div class="lab" v-if="education.lab">
      <font-awesome-icon class="icon" :icon="['fas', 'vial']" />
      {{ education.lab }}
    </div>
    <div class="faculty">
      <font-awesome-icon class="icon" :icon="['fas', 'school']" />
      {{ education.faculty }}
    </div>
    <div class="institution">
      <font-awesome-icon class="icon" :icon="['fas', 'university']" />
      {{ education.institution }}
    </div>
    <div class="location">
      <font-awesome-icon class="icon" :icon="['fas', 'map-marker-alt']" />
      {{ education.location }}
    </div>
    <div class="time">
      <font-awesome-icon class="icon" :icon="['fas', 'calendar']" />
      {{ education.time }}
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
    height: 45px;
    width: 40px;
    margin-bottom: 16px;
    margin-top: 40px;

    img {
      height: 100%;
      width: 100%;
    }
  }
}
</style>
