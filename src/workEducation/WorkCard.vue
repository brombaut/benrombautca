<template>
  <li class="work-card align-left slide-in">
    <div class="list-item-bullet" />
    <div class="list-item-content">
      <div class="list-item-item image-container">
        <img :src="imageSource" :alt="work.imageFile" />
      </div>
      <div class="list-item-item title">{{ work.title }}</div>
      <div class="list-item-item team" v-if="work.team">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'users']" />
        </div>
        <div>{{ work.team }}</div>
      </div>
      <div class="list-item-item company">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'building']" />
        </div>
        <a :href="work.link" target="_blank" rel="noopener noreferrer">{{ work.company }}</a>
      </div>
      <div class="list-item-item location">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'map-marker-alt']" />
        </div>
        <div>{{ work.location }}</div>
      </div>
      <div class="list-item-item time">
        <div class="icon-container">
          <font-awesome-icon class="icon" :icon="['fas', 'calendar']" />
        </div>
        <div>{{ work.time }}</div>
      </div>
    </div>
  </li>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import uiUtils from "@/utils/ui-utils";
import { Work } from "./work";

export default defineComponent({
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
    height: 52px;
    margin-bottom: 0px;
    margin-top: 32px;

    img {
      height: 100%;
      border-radius: 4px;
    }
  }

  .team {
    color: $primary !important;
    font-weight: bold;
  }
}
</style>
