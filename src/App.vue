<template>
  <div id="app">
      <NavBar />
      <MainContentContainer />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar/NavBar.vue';
import MainContentContainer from '@/components/MainContentContainer.vue';

export default {
    name: 'App',
    components: {
        NavBar,
        MainContentContainer,
    },
};
</script>

<style lang="scss">
#app {
    font-family: League Spartan,Helvetica,Arial,sans-serif;
    font-family: 'Share Tech Mono', Helvetica,Arial,sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    display: flex;
    height: 100%;
    width: 100%;
}
</style>
