<template>
  <div class="view-on-and-tech-used">
    <div class='icons-info'>
      <span>View On:</span>
      <div class='icon-container'>
        <div
          v-for="repo in software.externalRepos"
          :key="repo._id"
          class='icon'
          @click.stop.prevent="handleExternalProfileClicked(repo._url)">
          <img :src="imageSource(repo._imagePath)" />
          <span class="tooltip-text">{{repo._hoverText}}</span>
        </div>
      </div>
    </div>
    <div class='icons-info'>
      <span>Tech Used:</span>
      <div class='icon-container'>
        <div
          v-for="tech in software.techUsed"
          :key="tech._id"
          class='icon'>
          <img :src="imageSource(tech._imagePath)" />
          <span class="tooltip-text">{{tech._hoverText}}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { SoftwareArticle } from "./SoftwareArticlesProxy";
import uiUtils from "@/utils/ui-utils";

@Component
export default class ViewOnAndTechUsed extends Vue {

  @Prop()
  software!: SoftwareArticle;

  imageSource(imageName: string) {
    return uiUtils.loadImage(imageName);
  }

  private handleExternalProfileClicked(url: string) {
    if (url) {
      const result: Window | null = window.open(url, "_blank");
      if (result) {
        result.focus();
      }
    }
  }
}
</script>

<style lang="scss">
.view-on-and-tech-used {
  display: flex;
  flex-direction: row;

  .icons-info {
    display: flex;
    align-items: center;

    .icon-container{
      display: flex;
      align-items: center;
      background: $secondaryLightest;
      padding: 8px 8px 2px 8px;
      margin: 0 8px;
      border-radius: 8px;
      border: 1px solid $primaryDark;

      .icon {
        display: flex;
        position: relative;
        display: inline-block;

        .tooltip-text {
          visibility: hidden;
          width: 120px;
          top: calc(100% + 8px);
          left: 50%;
          margin-left: -60px;
          background-color: black;
          color: #fff;
          text-align: center;
          padding: 5px 0;
          border-radius: 6px;
          position: absolute;
          z-index: 1;
          opacity: 0;
          transition: opacity 0.3s;
        }

        .tooltip-text::after {
          content: " ";
          position: absolute;
          bottom: 100%;  /* At the top of the tooltip */
          left: 50%;
          margin-left: -5px;
          border-width: 5px;
          border-style: solid;
          border-color: transparent transparent black transparent;
        }

        img {
          height: 28px;
          margin: 0 8px;
          transition: transform 0.3s;
        }

        &:hover {
          .tooltip-text {
            visibility: visible;
            opacity: 1;
          }

          img {
            transform: scale(1.1);
          }
        }
      }
    }
  }
}
</style>
