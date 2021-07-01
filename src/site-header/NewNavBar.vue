<template>
  <header class="new-nav-bar header-dark">
    <div class="wrapper">
      <FullNavBar />
      <div class="condensed-navbar-icon">
        <font-awesome-icon :icon="['fas', 'bars']" class="nav-icon" @click="toggleMobileNavBar" />
      </div>
    </div>
    <nav class="condensed-navbar" ref="mobileNavbar" :class="{ showNavBar: mobileNavbarVisible }">
      <a @click="navigateMobile('/about-me')">
        <span>About Me</span>
        <span class="underline"></span>
      </a>
      <a @click="navigateMobile('/bookshelf')">
        <span>Bookshelf</span>
        <span class="underline"></span>
      </a>
      <a @click="navigateMobile('/articles')">
        <span>Articles</span>
        <span class="underline"></span>
      </a>
      <a @click="navigateMobile('/software')">
        <span>Software</span>
        <span class="underline"></span>
      </a>
    </nav>
  </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { bus } from "@/main";
import SiteHeader from "./SiteHeader.vue";
import FullNavBar from "./FullNavBar.vue";

@Component({
  components: {
    FullNavBar,
  },
})
export default class NewNavBar extends Vue {
  private enableActiveElHighlighter = false;

  private mobileNavbarVisible = false;

  private navBarEl!: HTMLElement;

  private startingNavBarOffset!: number;

  private activeRoutes: string[] = [];

  private navigate(routeName: string): void {
    if (routeName !== this.$route.path) {
      this.$router.push(routeName);
    }
    // this.setActiveRoutes([this.$route.name || ""]);
    // const activeEls: NodeListOf<HTMLElement> = this.$el.querySelectorAll(".active");
    // const activeNavClasses: DOMTokenList[] = [];
    // activeEls.forEach((el: HTMLElement) => {
    //   activeNavClasses.push(el.classList);
    // });
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
    if (window.pageYOffset >= this.startingNavBarOffset) {
      this.navBarEl.classList.add("sticky");
      (this.$parent as SiteHeader).addBottomMargin();
    } else {
      this.navBarEl.classList.remove("sticky");
      (this.$parent as SiteHeader).removeBottomMargin();
    }
  }

  private setActiveRoutes(newRoutes: string[]): void {
    this.activeRoutes = newRoutes;
  }

  mounted() {
    this.navBarEl = this.$el as HTMLElement;
    this.startingNavBarOffset = this.navBarEl.offsetTop;
    window.onscroll = () => this.watchStickyNav();
    bus.$on("routeChanged", this.setActiveRoutes);
    this.setActiveRoutes([this.$route.name || ""]);
  }
}
</script>

<style lang="scss">
.new-nav-bar {
  width: 100%;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 20;
  // box-shadow: 1px 5px 5px $pFontColor;

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

    .condensed-navbar-icon {
      display: none;
      align-items: center;
      margin: 8px 12px;

      .nav-icon {
        font-size: 2rem;

        &:hover {
          cursor: pointer;
        }
      }
    }

    @media only screen and (max-width: 640px) {
      justify-content: flex-end;

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
    background: $primaryDark;

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

  // TODO: Can this be moved into either condensed or full navbar?
  a {
    padding: 16px 28px;
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

    &.active {
      .underline {
        width: 100%;
      }
    }

    &:hover {
      cursor: pointer;
      text-decoration: none;

      .underline {
        width: 100%;
      }
    }
  }
}
</style>
