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
import { Component, Vue } from "vue-property-decorator";
import SiteFooter from "@/footer/SiteFooter.vue";
import SiteHeader from "@/site-header/SiteHeader.vue";

@Component({
  components: {
    SiteFooter,
    SiteHeader,
  },
})
export default class App extends Vue { }
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
  background: $secondary;
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
    max-width: 1100px;
    margin: 16px 0;
    padding: 16px;
    z-index: 2;
    background: $secondaryLight;
    border-radius: 4px;
    box-shadow: 1px 1px 5px $pFontColor;
  }
}
</style>
