<template>
  <header class="new-nav-bar header-dark" ref="navHeader">
    <div class="wrapper">
      <FullNavBar />
      <div class="condensed-navbar-left">
        <BackButton />
        <span v-if="!isDetailPage" class="current-section-label">{{ currentSectionLabel }}</span>
      </div>
      <div
        class="condensed-navbar-icon"
        role="button"
        tabindex="0"
        :aria-expanded="mobileNavbarVisible"
        aria-label="Toggle navigation menu"
        @click="toggleMobileNavBar"
        @keydown.enter="toggleMobileNavBar">
        <font-awesome-icon :icon="['fas', mobileNavbarVisible ? 'xmark' : 'bars']" class="nav-icon" />
      </div>
    </div>
    <CondensedNavBar
      :mobileNavbarVisible="mobileNavbarVisible"
      @closeMobileNavBar="closeMobileNavBar" />
  </header>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import FullNavBar from "./FullNavBar.vue";
import CondensedNavBar from "./CondensedNavBar.vue";
import BackButton from "./BackButton.vue";

interface SiteHeader {
  addBottomMargin(): void;
  removeBottomMargin(): void;
}

export default defineComponent({
  name: "NewNavBar",
  components: {
    FullNavBar,
    CondensedNavBar,
    BackButton,
  },
  data() {
    return {
      mobileNavbarVisible: false,
      startingNavBarOffset: 0,
      boundHandleOutsideClick: null as ((e: MouseEvent) => void) | null,
      boundWatchStickyNav: null as (() => void) | null,
    };
  },
  computed: {
    currentSectionLabel(): string {
      const routeName = this.$route.name as string;
      const labels: Record<string, string> = {
        land: "About Me",
        aboutMe: "About Me",
        work: "About Me",
        education: "About Me",
        publications: "Publications",
        bookshelf: "Bookshelf",
        articles: "Articles",
        selectedArticle: "Articles",
        software: "Software",
        selectedSoftware: "Software",
        running: "Running",
        hiking: "Hiking",
      };
      return labels[routeName] || "";
    },
    isDetailPage(): boolean {
      const routeName = this.$route.name as string;
      return routeName === "selectedArticle" || routeName === "selectedSoftware";
    },
  },
  methods: {
    toggleMobileNavBar(): void {
      this.mobileNavbarVisible = !this.mobileNavbarVisible;
    },
    closeMobileNavBar(): void {
      this.mobileNavbarVisible = false;
    },
    handleOutsideClick(event: MouseEvent): void {
      const navHeader = this.$refs.navHeader as HTMLElement;
      if (this.mobileNavbarVisible && navHeader && !navHeader.contains(event.target as Node)) {
        this.closeMobileNavBar();
      }
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
    this.boundWatchStickyNav = () => this.watchStickyNav();
    this.boundHandleOutsideClick = (e: MouseEvent) => this.handleOutsideClick(e);
    window.addEventListener("scroll", this.boundWatchStickyNav);
    document.addEventListener("click", this.boundHandleOutsideClick);
  },
  beforeUnmount() {
    if (this.boundWatchStickyNav) {
      window.removeEventListener("scroll", this.boundWatchStickyNav);
    }
    if (this.boundHandleOutsideClick) {
      document.removeEventListener("click", this.boundHandleOutsideClick);
    }
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

    .condensed-navbar-left {
      display: none;
      align-items: center;
      margin-right: auto;
      padding-left: 12px;

      .current-section-label {
        font-weight: 600;
        font-size: 1.1em;
        margin-left: 8px;
      }
    }

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

    @media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
      justify-content: space-between;

      .full-navbar {
        display: none;
      }

      .condensed-navbar-left {
        display: flex;
      }

      .condensed-navbar-icon {
        display: flex;
      }
    }
  }

}
</style>
