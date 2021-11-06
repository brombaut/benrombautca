<template>
  <div class="tag" :style="tagStyle"><b>{{ tag }}</b></div>
</template>

<script lang="ts">
import Vue from "vue";
import TagColor from "./TagColor";

export default Vue.extend({
  name: "Tag",
  props: {
    tag: String,
  },
  computed: {
    tagStyle(): Object {
      return {
        backgroundColor: this.tagColors.backgroundColor,
        color: this.tagColors.color,
      };
    },
    tagColors(): TagColor {
      switch (this.$props.tag) {
      case ("how-to"): return new TagColor("rgb(254, 255, 165)", "rgb(179, 0, 71)");
      case ("init"): return new TagColor("rgb(245, 57, 0)", "rgb(255, 255, 255)");
      case ("notes"): return new TagColor("#d6d9e0", "#606570");
      case ("typescript"): return new TagColor("rgb(35, 74, 132)", "rgb(255, 255, 255)");
      case ("npm"): return new TagColor("rgb(137, 6, 6)", "rgb(255, 255, 255)");
      case ("publish"): return new TagColor("rgb(86, 39, 101)", "rgb(255, 255, 255)");
      case ("deploy"): return new TagColor("rgb(6, 181, 0)", "rgb(255, 255, 255)");
      case ("github-actions"): return new TagColor("rgb(247, 223, 30)", "rgb(0, 0, 0)");
      case ("github-pages"): return new TagColor("rgb(86, 39, 101)", "rgb(255, 255, 255)");
      case ("statistics"): return new TagColor("rgb(237, 21, 86)", "rgb(255, 255, 255)");
      case ("example-repo"): return new TagColor("rgb(17, 58, 98)", "rgb(255, 255, 255)");
      case ("software-architecture"): return new TagColor("rgb(0, 0, 0)", "rgb(255, 255, 255)");
      case ("design-patterns"): return new TagColor("rgb(41, 101, 241)", "rgb(255, 255, 255)");
      case ("codecov"): return new TagColor("rgb(87, 215, 0)", "rgb(255, 255, 255)");
      case ("testing"): return new TagColor("rgb(0, 131, 53)", "rgb(255, 255, 255)");
      case ("cron"): return new TagColor("rgb(0, 0, 0)", "rgb(255, 255, 255)");
      case ("scheduled"): return new TagColor("rgb(224, 235, 245)", "rgb(4, 60, 111)");
      case ("correlation"): return new TagColor("rgb(42, 37, 102)", "rgb(255, 255, 255)");
      case ("residuals"): return new TagColor("rgb(108, 0, 185)", "rgb(255, 255, 255)");
      case ("linear-regression"): return new TagColor("rgb(34, 34, 34)", "rgb(97, 218, 246)");
      case ("bash"): return new TagColor("rgb(163, 45, 42)", "rgb(255, 255, 255)");
      case ("command-line"): return new TagColor("#282828", "#33ff33");
      case ("linux"): return new TagColor("rgb(23, 88, 135)", "rgb(247, 247, 247)");
      case ("tensorflow"): return new TagColor("rgb(247, 247, 247)", "rgb(230, 139, 35)");
      case ("machine-learning"): return new TagColor("rgb(206, 28, 57)", "rgb(247, 247, 247)");
      case ("deep-learning"): return new TagColor("rgb(71, 141, 193)", "rgb(210, 99, 165)");
      case ("software-design"): return new TagColor("rgb(51, 84, 108)", "rgb(247, 247, 247)");
      case ("pandas"): return new TagColor("#130654", "rgb(247, 247, 247)");
      case ("jupyter"): return new TagColor("#E46E2E", "rgb(51, 51, 51)");
      case ("data-analysis"): return new TagColor("rgb(237, 21, 86)", "rgb(247, 247, 247)");
      case ("python"): return new TagColor("#4b8bbe", "#ffd43b");
      case ("scikit-learn"): return new TagColor("rgb(240, 149, 56)", "rgb(50, 148, 199)");
      default: return new TagColor("#1d5ca4", "#f1f5fa");
      }
    },
  },
});
</script>

<style lang="scss">
.tag {
  font-size: 0.9em;
  font-weight: normal;
  margin: 4px 0;
  margin-right: 8px;
  padding: 6px 8px;
  border-radius: 6px;
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .tag {
    font-size: 0.7em;
    margin-right: 8px;
    padding: 4px 8px;
  }
}
</style>
