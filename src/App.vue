<template>
  <div id="app">
    <SiteHeader />
    <main>
      <router-view />
    </main>
    <SiteFooter />
  </div>
</template>

<script lang="ts">
import SiteFooter from "@/footer/SiteFooter.vue";
import SiteHeader from "@/site-header/SiteHeader.vue";

export default {
  name: "App",
  components: {
    SiteFooter,
    SiteHeader,
  },
};
</script>

<style lang="scss">
html,
body {
  margin: 0;
  background: $secondary;
  min-height: 100vh;
}
h1,h2,h3,h4,h5,h6 {
  margin: 0;
}

#app {
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $pFontColor;
  background: $aliceBlue;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  overflow-y: auto;
  overflow-x: auto;
  position: relative;
  min-height: 100vh;

  main {
    flex: 1;
  }

  section {
    max-width: $MAX_SECTION_SIZE;
    margin: 16px 4px;
    padding: 16px;
    z-index: 2;
    background: $secondaryLight;
    border-radius: 4px;
    border: 1px solid $secondaryDark;
    text-align: left;
    box-sizing: border-box;
  }
}
</style>
