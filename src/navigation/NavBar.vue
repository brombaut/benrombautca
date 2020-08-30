<template>
  <header class="nav-bar">
    <div class="wrapper">
      <h1>
        <a :class="{ active: curRoute === 'landing' }" @click="navigate('/')">
          <span>BEN ROMBAUT</span>
          <span class="underline"></span>
        </a>
      </h1>
      <nav class="full-navbar">
        <a :class="{ active: curRoute === 'aboutMe' }" @click="navigate('/about-me')">
          <span>ABOUT ME</span>
          <span class="underline"></span>
        </a>
        <a
          class="projects-route"
          :class="{ active: curRoute === 'projects' }"
          @click="navigate('/projects')"
        >
          <span>PROJECTS</span>
          <span class="underline"></span>
        </a>
        <a :class="{ active: curRoute === 'bookshelf' }" @click="navigate('/bookshelf')">
          <span>BOOKSHELF</span>
          <span class="underline"></span>
        </a>
        <!-- <a :class="{'active': curRoute === 'roadmaps'}" @click="navigate('/roadmaps')">
          <span>ROADMAPS</span>
          <span class="underline"></span>
        </a>-->
      </nav>
      <div class="condensed-navbar-icon">
        <font-awesome-icon :icon="['fas', 'bars']" class="nav-icon" @click="toggleMobileNavBar" />
      </div>
    </div>
    <nav class="condensed-navbar" ref="mobileNavbar" :class="{ showNavBar: mobileNavbarVisible }">
      <a :class="{ active: curRoute === 'aboutMe' }" @click="navigateMobile('/about-me')">
        <span>ABOUT ME</span>
        <span class="underline"></span>
      </a>
      <a
        class="projects-route"
        :class="{ active: curRoute === 'projects' }"
        @click="navigateMobile('/projects')"
      >
        <span>PROJECTS</span>
        <span class="underline"></span>
      </a>
      <a :class="{ active: curRoute === 'bookshelf' }" @click="navigateMobile('/bookshelf')">
        <span>BOOKSHELF</span>
        <span class="underline"></span>
      </a>
      <!-- <a :class="{'active': curRoute === 'roadmaps'}" @click="navigateMobile('/roadmaps')">
        <span>ROADMAPS</span>
        <span class="underline"></span>
      </a>-->
    </nav>
  </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class NavBar extends Vue {
  private mobileNavbarVisible = false;

  private navigate(routeName: string): void {
    if (routeName === this.$route.path) {
      return;
    }
    this.$router.push(routeName);
  }

  private navigateMobile(routeName: string): void {
    this.toggleMobileNavBar();
    this.navigate(routeName);
  }

  private toggleMobileNavBar(): void {
    this.mobileNavbarVisible = !this.mobileNavbarVisible;
  }

  get curRoute(): string {
    return this.$route.name || "";
  }

  get curRouteName(): string {
    if (this.curRoute === "aboutMe") {
      return "ABOUT ME";
    }
    if (this.curRoute === "PROJECTS") {
      return "PROJECTS";
    }
    if (this.curRoute === "bookshelf") {
      return "BOOKSHELF";
    }
    if (this.curRoute === "roadmaps") {
      return "ROADMAPS";
    }
    return "";
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
  position: relative;

  .wrapper {
    width: calc(100% - 16px);
    max-width: 1280px;
    display: flex;
    justify-content: space-between;
    position: relative;

    h1 {
      a {
        margin: 0;

        &.active {
          .underline {
            width: 100%;
          }
        }
      }
    }

    .full-navbar {
      display: flex;
      align-items: center;
    }

    .condensed-navbar-icon {
      display: none;
      align-items: center;
      margin: 0 12px;

      .nav-icon {
        font-size: 2rem;

        &:hover {
          cursor: pointer;
        }
      }
    }

    @media only screen and (max-width: 640px) {
      .full-navbar {
        display: none;
      }

      .condensed-navbar-icon {
        display: flex;
      }
    }
  }

  .condensed-navbar {
    display: none;
    position: absolute;
    background-color: $primaryDarkest;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    padding: 12px 16px;
    z-index: 99;
    width: 100%;
    top: 100%;
    flex-direction: column;
    align-items: flex-start;

    &.showNavBar {
      display: flex;
    }
  }

  @media only screen and (min-width: 640px) {
    .condensed-navbar {
      display: none;

      &.showNavBar {
        display: none;
      }
    }
  }

  a {
    margin: 12px;
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

  @media only screen and (max-width: 1200px) {
    .projects-route {
      display: none;
    }
  }
}
</style>
