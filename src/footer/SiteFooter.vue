<template>
  <footer class="site-footer">
    <div class="wrapper">
      <div>Created By Ben Rombaut</div>
      <div class="dash">-</div>
      <div>Last Updated {{ lastDeployed }}</div>
    </div>
  </footer>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import lastDeployed from "./last-deployed";

@Component
export default class SiteFooter extends Vue {
  private lastDeployed: string = lastDeployed;
}
</script>

<style lang="scss">
.site-footer {
  color: $primaryDark;
  // margin-bottom: 16px;
  display: flex;
  justify-content: center;
  width: 100%;
  background: $primaryDarkest;
  // padding: 16px;

  .wrapper {
    width: calc(100% - 16px);
    max-width: 1280px;
    display: flex;
    justify-content: center;
    padding: 32px 0;
    color: white;

    .dash {
      margin: 0 4px;
    }
  }
}
</style>
