<template>
  <footer class="site-footer">
    <div class="wrapper">
      <div>Created By Ben Rombaut</div>
    </div>
  </footer>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "SiteFooter",
});
</script>

<style lang="scss">
.site-footer {
  color: $primaryDark;
  display: flex;
  justify-content: center;
  width: 100%;
  background: $primaryDarkest;

  .wrapper {
    width: calc(100% - 16px);
    max-width: 1280px;
    display: flex;
    justify-content: center;
    padding: 32px 0;
    color: white;

  }
}
</style>
