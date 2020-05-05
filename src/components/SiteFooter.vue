<template>
  <footer class="site-footer">
    <div>Created By Ben Rombaut</div>
    <div class="dash">-</div>
    <div>Last Updated {{ lastDeployed }}</div>
  </footer>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import lastDeployed from "@/data/last-deployed";

@Component
export default class SiteFooter extends Vue {
  private lastDeployed: string = lastDeployed;
}
</script>

<style lang="scss">
.site-footer {
  color: $primaryDark;
  margin-bottom: 16px;
  display: flex;

  .dash {
    margin: 0 4px;
  }
}
</style>
