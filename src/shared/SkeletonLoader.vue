<template>
  <div class="skeleton">
    <div
      v-show="imageLoading"
      :class="classObject"
      class="skeleton__loader">
    </div>
    <img
      v-show="!imageLoading"
      :src="imageSource()"
      :alt="imageAlt"
      :class="{'circle': isCircle}"/>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import uiUtils from "@/utils/ui-utils";

export default defineComponent({
  name: "SkeletonLoader",
  props: {
    imagePath: {
      type: String,
      required: true,
    },
    imageAlt: {
      type: String,
      required: true,
    },
    isCircle: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      imageLoading: true,
    };
  },
  computed: {
    classObject(): Object {
      return {
        skeleton__loader: true,
        circle: this.$props.isCircle,
      };
    },
  },
  methods: {
    imageSource(): any {
      const result = uiUtils.loadImage(this.$props.imagePath);
      this.imageLoading = false;
      return result;
    },
  },
});
</script>

<style lang="scss">

.skeleton {
  height: 100%;
  width: 100%;

  .circle {
    border-radius: 50%;
  }

  .skeleton__loader {
    height: 100%;
    width: 100%;
    background-image: linear-gradient(90deg, $secondary 0px, $secondaryLightest 40px, $secondary 80px);
    animation: shine-header 1.6s infinite linear;;
  }

  @keyframes shine-header {
    0% {
      background-position: -100px;
    }
    40%,
    100% {
      background-position: 270px;
    }
  }

  img {
    height: 100%;
    width: 100%;
  }
}

</style>
