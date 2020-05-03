<template>
  <div id="app"></div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class App extends Vue {}
</script>

<style lang="scss">
#app {
  font-family: League Spartan, Helvetica, Arial, sans-serif;
  font-family: "Share Tech Mono", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
  background: $secondaryDark;
  display: flex;
  height: 100%;
  width: 100%;
}
</style>
