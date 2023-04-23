<template>
  <div class="tech-used-icon" :style="tagStyle">
    <img :src="imageSource(tech._imagePath)" />
    <div class="label"><b>{{ tech._title }}</b></div>
  </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import uiUtils from "@/utils/ui-utils";
import { Tech } from "./SoftwareArticlesProxy";
import TagColor from "@/shared/TagColor";

export default defineComponent({
  name: "TechUsedIcon",
  props: {
    tech: {
      type: Object as PropType<Tech>,
      required: true,
    },
  },
  computed: {
    tagStyle(): Object {
      return {
        backgroundColor: this.tagColors.backgroundColor,
        color: this.tagColors.color,
      };
    },
    tagColors(): TagColor {
      switch (this.$props.tech._title) {
      case ("TypeScript"): return new TagColor("#007acc", "#ffffff");
      case ("Vue"): return new TagColor("#35495e", "#42b883");
      case ("Python"): return new TagColor("#4b8bbe", "#ffd43b");
      case ("Firebase"): return new TagColor("rgb(3, 156, 229)", "rgb(255, 203, 45)");
      case ("Node"): return new TagColor("#303030", "#68a063");
      default: return new TagColor("#1d5ca4", "#f1f5fa");
      }
    },
  },
  methods: {
    imageSource(imageName: string): any {
      return uiUtils.loadImage(imageName);
    },
  },
});
</script>

<style lang="scss">
.tech-used-icon {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 4px;
  margin: 4px 12px 4px 0px;
  border-radius: 6px;

  img {
    height: 24px;
    width: 24px;
    margin: 0 4px;
  }

  .label {
    margin: 0 4px;
  }
}
@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .tech-used-icon {
    margin-right: 8px;

    img {
      height: 20px;
      width: 20px;
    }

    .label {
      font-size: 0.8em;
    }
  }
}
</style>
