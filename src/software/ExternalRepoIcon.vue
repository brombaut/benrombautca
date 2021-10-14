<template>
  <div class="external-repo-icon">
    <a
      v-if="verbose"
      class="link-verbose"
      :style="tagStyle"
      :href="externalRepo._url"
      @click.stop.prevent="handleExternalProfileClicked(externalRepo._url)">
      <img :src="imageSource(externalRepo._imagePath)" />
      <div class="label">
        {{ externalRepo._hoverText }}
        <font-awesome-icon
          :icon="['fas', 'external-link-alt']"
          :style="tagStyle" />
      </div>
    </a>
    <a
      v-else
      class="link"
      :href="externalRepo._url"
      @click.stop.prevent="handleExternalProfileClicked(externalRepo._url)">
      <img :src="imageSource(externalRepo._imagePath)" />
      <div class="hover"></div>
    </a>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import uiUtils from "@/utils/ui-utils";
import { ExternalRepo } from "./SoftwareArticlesProxy";
import TagColor from "@/shared/TagColor";

export default Vue.extend({
  name: "ExternalRepoIcon",
  props: {
    externalRepo: {
      type: Object as PropType<ExternalRepo>,
      required: true,
    },
    verbose: {
      type: Boolean,
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
      switch (this.$props.externalRepo._title) {
      case ("GitHub"): return new TagColor("#403d3d", "#ffffff");
      case ("NPM"): return new TagColor("#cc3534", "#ffffff");
      default: return new TagColor("#1d5ca4", "#f1f5fa");
      }
    },
  },
  methods: {
    imageSource(imageName: string): any {
      return uiUtils.loadImage(imageName);
    },
    handleExternalProfileClicked(url: string): void {
      if (url) {
        const result: Window | null = window.open(url, "_blank");
        if (result) {
          result.focus();
        }
      }
    },
  },
});
</script>

<style lang="scss">
.external-repo-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-right: 12px;

  a {
    &:hover {
      cursor: pointer;
    }
  }

  .link {
    position: relative;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;

    .hover {
      position: absolute;
      background-color: $secondary;
      height: 0%;
      width: 0%;
      border-radius: 8px;
      z-index: 0;
      transition: all 0.2s;
    }

    img {
      padding: 6px;
      height: 36px;
      width: 36px;
      z-index: 1;
      border-radius: 12px;
    }

    &:hover {
      .hover {
        height: 100%;
        width: 100%;
      }
    }
  }

  .link-verbose {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0 6px;
    margin: 4px 4px 4px 0px;
    border-radius: 6px;

    img {
      padding: 4px;
      height: 28px;
      width: 28px;
      z-index: 1;
      border-radius: 12px;
    }

    .label {
      margin: 0 4px;
    }
  }
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .external-repo-icon {
    margin-right: 8px;

    .link {
      img {
        padding: 4px;
        height: 28px;
        width: 28px;
      }
    }

    .link-verbose {
      img {
        height: 20px;
        width: 20px;
      }

      .label {
        font-size: 0.8em;
      }
    }
  }
}

</style>
