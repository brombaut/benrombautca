<template>
  <header id="site-header" class="header-bright">
    <div class="banner">
      <h1><b>BEN ROMBAUT</b></h1>
      <h4><i>Master of Science Candidate at the Software Analysis & Intelligence Lab, Queen's University</i></h4>
    </div>
    <NavBar />
  </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NavBar from "@/site-header/NavBar.vue";

@Component({
  components: {
    NavBar,
  },
})
export default class SiteHeader extends Vue {
}
</script>

<style lang="scss">
#site-header {
  width: 100%;
  display: flex;
  flex-direction: column;

  .banner {
    padding: 32px 0;
  }

  h1 {
    margin: 8px 0;
    font-size: 3.5rem;
  }

  h4 {
    margin: 4px 0;
  }
}
</style>
