<template>
  <header class="nav-bar header-dark">
    <div class="wrapper">
      <nav class="full-navbar">
        <a :class="{ active: curRoute === 'aboutMe' }" @click="navigate('/about-me')">
          <span>ABOUT ME</span>
          <span class="underline"></span>
        </a>
        <a :class="{ active: curRoute === 'work' }" @click="navigate('/work')">
          <span>WORK</span>
          <span class="underline"></span>
        </a>
        <a :class="{ active: curRoute === 'education' }" @click="navigate('/education')">
          <span>EDUCATION</span>
          <span class="underline"></span>
        </a>
        <a :class="{ active: curRoute === 'bookshelf' }" @click="navigate('/bookshelf')">
          <span>BOOKSHELF</span>
          <span class="underline"></span>
        </a>
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
      <a :class="{ active: curRoute === 'bookshelf' }" @click="navigateMobile('/bookshelf')">
        <span>BOOKSHELF</span>
        <span class="underline"></span>
      </a>
    </nav>
  </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { bus } from "@/main";
import SiteHeader from "./SiteHeader.vue";

@Component
export default class NavBar extends Vue {
  private mobileNavbarVisible = false;

  private navBarEl!: HTMLElement;

  private startingNavBarOffset!: number;

  private navigate(routeName: string): void {
    if (routeName !== this.$route.path) {
      this.$router.push(routeName);
    }
    bus.$emit("routeClicked");
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

  private watchStickyNav(): void {
    const yOffset = window.pageYOffset;
    if (window.pageYOffset >= this.startingNavBarOffset) {
      this.navBarEl.classList.add("sticky");
      (this.$parent as SiteHeader).addBottomMargin();
    } else {
      this.navBarEl.classList.remove("sticky");
      (this.$parent as SiteHeader).removeBottomMargin();
    }
  }

  mounted() {
    this.navBarEl = this.$el as HTMLElement;
    this.startingNavBarOffset = this.navBarEl.offsetTop;
    window.onscroll = () => this.watchStickyNav();
  }
}
</script>

<style lang="scss">
.nav-bar {
  width: 100%;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 20;
  box-shadow: 1px 1px 5px $pFontColor;

  &.sticky {
    position: fixed;
    top: 0;
  }

  .wrapper {
    width: calc(100% - 16px);
    max-width: 1280px;
    display: flex;
    justify-content: center;
    position: relative;

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
    margin: 16px 28px;
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
      text-decoration: none;

      .underline {
        width: 100%;
      }
    }

    // &.active {
    //   .underline {
    //     width: 100%;
    //   }
    // }
  }

  @media only screen and (max-width: 1200px) {
    .projects-route {
      display: none;
    }
  }
}
</style>
