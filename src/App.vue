<template>
  <div id="app">
      <NavBar />
      <Home />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import Home from '@/components/Home.vue';

export default {
    name: 'App',
    components: {
        NavBar,
        Home,
    },
};
</script>

<style lang="scss">
#app {
//   font-family: Avenir, Helvetica, Arial, sans-serif;
    font-family: League Spartan,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    display: flex;
    height: 100%;
    width: 100%;
}
</style>
