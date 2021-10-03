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
import Vue from "vue";
// import SiteHeader from "./SiteHeader.vue";
import FullNavBar from "./FullNavBar.vue";
import CondensedNavBar from "./CondensedNavBar.vue";

interface SiteHeader {
  addBottomMargin(): void;
  removeBottomMargin(): void;
}

export default Vue.extend({
  name: "NewNavBar",
  components: {
    FullNavBar,
    CondensedNavBar,
  },
  data() {
    return {
      mobileNavbarVisible: false,
      startingNavBarOffset: 0,
    };
  },
  methods: {
    toggleMobileNavBar(): void {
      this.mobileNavbarVisible = !this.mobileNavbarVisible;
    },
    closeMobileNavBar(): void {
      this.mobileNavbarVisible = false;
    },
    watchStickyNav(): void {
      // TODO: Fix these type conversions
      if (window.pageYOffset >= this.startingNavBarOffset) {
        this.$el.classList.add("sticky");
        (this.$parent as unknown as SiteHeader).addBottomMargin();
      } else {
        this.$el.classList.remove("sticky");
        (this.$parent as unknown as SiteHeader).removeBottomMargin();
      }
    },
  },
  mounted() {
    this.startingNavBarOffset = (this.$el as HTMLElement).offsetTop;
    window.onscroll = () => this.watchStickyNav();
  },
});
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
