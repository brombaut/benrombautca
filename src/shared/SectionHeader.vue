<template>
  <header class="section-header">
    <div class="section-header_wrapper">
      <div class="section-header_content">
        <font-awesome-icon class="icon" :icon="['fas', icon]" v-if="icon" />
        <h1 class="section-title">{{ title }}</h1>
      </div>
      <div class="section-header-underline" />
    </div>
    <p v-if="subtext">{{ subtext }}</p>
  </header>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "SectionHeader",
  props: {
    title: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      default: "",
    },
    subtext: {
      type: String,
      default: "",
    },
  },
});
</script>

<style lang="scss">
.section-header {
  display: flex;
  flex-direction: column;
  width: fit-content;
  // margin-bottom: 16px;

  .section-header_wrapper {
    width: fit-content;
    display: flex;
    flex-direction: column;

    .section-header_content {
      display: flex;
      flex-direction: row;
      transition: 0.3s color;
      font-size: 1.5rem;
      align-items: center;
      line-height: 2;
      color: $primaryDark;

      .section-title {
        margin: 0 16px;
        text-align: left;
      }

      @media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
        .section-title {
          font-size: 1.7rem;
        }
      }

      .icon {
        font-size: 1.5em;
      }
    }

    .section-header-underline {
      background: $primaryDark;
      height: 4px;
    }
  }
}
</style>
