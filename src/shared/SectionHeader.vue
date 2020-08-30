<template>
  <header class="section-header">
    <div class="section-header_content">
      <font-awesome-icon :icon="['fas', icon]" />
      <h1 class="section-title">{{ title }}</h1>
    </div>
    <div class="section-header-underline"></div>
  </header>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class SectionHeader extends Vue {
  @Prop()
  title!: string;

  @Prop()
  icon!: string;
}
</script>

<style lang="scss">
.section-header {
  display: flex;
  flex-direction: column;
  padding: 16px 0;
  width: fit-content;
  margin-bottom: 16px;

  .section-header_content {
    display: flex;
    flex-direction: row;
    transition: 0.3s color;
    font-size: 1.5rem;
    align-items: center;
    line-height: 2;

    .section-title {
      margin: 0 16px;
      text-align: left;
    }

    @media only screen and (max-width: 600px) {
      .section-title {
        font-size: 1.7rem;
      }
    }
  }

  .section-header-underline {
    background: $primary;
    height: 4px;
  }
}
</style>
