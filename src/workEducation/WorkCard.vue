<template>
  <li class="work-card align-left slide-in">
    <div class="image-container">
      <img :src="imageSource" :alt="work.imageFile" />
    </div>
    <div class="title">{{ work.title }}</div>
    <div class="team" v-if="work.team">
      <font-awesome-icon class="icon" :icon="['fas', 'users']" />
      {{ work.team }}
    </div>
    <div class="company">
      <font-awesome-icon class="icon" :icon="['fas', 'building']" />
      <a :href="work.link" target="_blank">{{ work.company }}</a>
    </div>
    <div class="location">
      <font-awesome-icon class="icon" :icon="['fas', 'map-marker-alt']" />
      {{ work.location }}
    </div>
    <div class="time">
      <font-awesome-icon class="icon" :icon="['fas', 'calendar']" />
      {{ work.time }}
    </div>
  </li>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import uiUtils from "@/utils/ui-utils";
import { Work } from "./work";

export default Vue.extend({
  name: "WorkCard",
  props: {
    work: {
      type: Object as PropType<Work>,
      required: true,
    },
  },
  computed: {
    imageSource(): any {
      return uiUtils.loadImage(this.$props.work.imageFile);
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
.work-card {

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

  .team {
    color: $primary !important;
    font-weight: bold;
  }

  .company {
    a {
      margin-left: 4px;
    }
  }
}
</style>
