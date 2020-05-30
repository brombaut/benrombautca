<template>
  <header class="nav-bar">
    <div class="wrapper">
      <h1>BEN ROMBAUT</h1>
      <nav>
        <a @click="navigate('/')">ABOUT ME</a>
        <!-- <a @click="navigate('/work-education')">WORK & EDUCATION</a> -->
        <a @click="navigate('/projects')">PROJECTS</a>
        <a @click="navigate('/bookshelf')">BOOKSHELF</a>
        <a @click="navigate('/roadmaps')">ROADMAPS</a>
      </nav>
    </div>
  </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class NavBar extends Vue {
  private navigate(routeName: string): void {
    if (routeName === this.$route.path) {
      return;
    }
    this.$router.push(routeName);
  }
}
</script>

<style lang="scss">
.nav-bar {
  width: 100%;
  background: $primaryDark;
  display: flex;
  justify-content: center;

  .wrapper {
    width: calc(100% - 16px);
    max-width: 1280px;
    display: flex;
    justify-content: space-between;

    nav {
      display: flex;
      align-items: center;

      a {
        margin: 0 12px;

        &:hover {
          cursor: pointer;
          text-decoration: underline;
        }
      }
    }
  }
}
</style>
