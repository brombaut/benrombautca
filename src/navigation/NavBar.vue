<template>
  <header class="nav-bar">
    <div class="wrapper">
      <h1>BEN ROMBAUT</h1>
      <nav>
        <a :class="{'active': curRoute === 'aboutMe'}" @click="navigate('/')">
          <span>ABOUT ME</span>
          <span class="underline"></span>
        </a>
        <a :class="{'active': curRoute === 'projects'}" @click="navigate('/projects')">
          <span>PROJECTS</span>
          <span class="underline"></span>
        </a>
        <a :class="{'active': curRoute === 'bookshelf'}" @click="navigate('/bookshelf')">
          <span>BOOKSHELF</span>
          <span class="underline"></span>
        </a>
        <a :class="{'active': curRoute === 'roadmaps'}" @click="navigate('/roadmaps')">
          <span>ROADMAPS</span>
          <span class="underline"></span>
        </a>
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

  get curRoute(): string {
    return this.$route.name || "";
  }
}
</script>

<style lang="scss">
.nav-bar {
  width: 100%;
  background: $primaryDark;
  display: flex;
  justify-content: center;
  color: $hFontColor;

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
        display: flex;
        flex-direction: column;
        align-items: center;
        font-weight: bold;

        .underline {
          background: white;
          height: 4px;
          width: 0;
          border-radius: 4px;
          margin-top: 2px;
          transition: 0.2s all ease-in;
        }

        &:hover {
          cursor: pointer;

          .underline {
            width: 100%;
          }
        }

        &.active {
          .underline {
            width: 100%;
          }
        }
      }
    }
  }
}
</style>
