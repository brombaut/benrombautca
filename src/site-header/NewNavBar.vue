<template>
  <header class="new-nav-bar header-dark">
    <div class="wrapper">
      <FullNavBar />
      <div class="condensed-navbar-icon">
        <font-awesome-icon :icon="['fas', 'bars']" class="nav-icon" @click="toggleMobileNavBar" />
      </div>
    </div>
    <CondensedNavBar :mobileNavbarVisible="mobileNavbarVisible" @closeMobileNavBar="closeMobileNavBar"/>
  </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SiteHeader from "./SiteHeader.vue";
import FullNavBar from "./FullNavBar.vue";
import CondensedNavBar from "./CondensedNavBar.vue";

@Component({
  components: {
    FullNavBar,
    CondensedNavBar,
  },
})
export default class NewNavBar extends Vue {

  private mobileNavbarVisible = false;

  private navBarEl!: HTMLElement;

  private startingNavBarOffset!: number;

  private toggleMobileNavBar(): void {
    this.mobileNavbarVisible = !this.mobileNavbarVisible;
  }

  private closeMobileNavBar(): void {
    this.mobileNavbarVisible = false;
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

  mounted() {
    this.navBarEl = this.$el as HTMLElement;
    this.startingNavBarOffset = this.navBarEl.offsetTop;
    window.onscroll = () => this.watchStickyNav();
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

  &.sticky {
    position: fixed;
    top: 0;
  }

  .wrapper {
    width: 100%;
    max-width: $MAX_SECTION_SIZE;
    display: flex;
    justify-content: center;
    position: relative;

    .condensed-navbar-icon {
      display: none;
      align-items: center;
      margin: 4px 12px;

      .nav-icon {
        font-size: 2em;

        &:hover {
          cursor: pointer;
        }
      }
    }

    @media only screen and (max-width: $PHONE_DISPLAY_SIZE) {
      justify-content: flex-end;

      .full-navbar {
        display: none;
      }

      .condensed-navbar-icon {
        display: flex;
      }
    }
  }

}
</style>
