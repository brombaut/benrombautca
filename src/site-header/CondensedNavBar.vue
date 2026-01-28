<template>
  <nav
    class="condensed-navbar"
    ref="mobileNavbar"
    :class="{ showNavBar: mobileNavbarVisible }"
    role="navigation"
    aria-label="Mobile navigation">
    <a
      v-for="item in navItems"
      :key="item.route"
      tabindex="0"
      role="menuitem"
      @click="navigateMobile(item.path)"
      @keydown.enter="navigateMobile(item.path)">
      <font-awesome-icon
        class='active-icon'
        :class="{ active: routeIsActive(item.route) }"
        :icon="['fas', 'chevron-right']" />
      <span>{{ item.label }}</span>
    </a>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface NavItem {
  path: string;
  route: string;
  label: string;
}

export default defineComponent({
  props: {
    mobileNavbarVisible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    const navItems: NavItem[] = [
      { path: "/about-me", route: "aboutMe", label: "About Me" },
      { path: "/publications", route: "publications", label: "Publications" },
      { path: "/bookshelf", route: "bookshelf", label: "Bookshelf" },
      { path: "/articles", route: "articles", label: "Articles" },
      // { path: "/software", route: "software", label: "Software" },
      { path: "/running", route: "running", label: "Running" },
      { path: "/hiking", route: "hiking", label: "Hiking" },
    ];
    return {
      navItems,
    };
  },
  methods: {
    navigateMobile(routePath: string): void {
      this.$emit("closeMobileNavBar");
      this.navigate(routePath);
    },
    navigate(routePath: string): void {
      if (routePath !== this.$route.path) {
        this.$router.push(routePath);
      }
    },
    routeIsActive(routeName: string): boolean {
      switch (routeName) {
      case ("aboutMe"): return this.$route.name === routeName || this.$route.name === "land";
      case ("articles"): return this.$route.name === routeName || this.$route.name === "selectedArticle";
      case ("software"): return this.$route.name === routeName || this.$route.name === "selectedSoftware";
      default: return this.$route.name === routeName;
      }
    },
  },
});
</script>

<style lang="scss">
.condensed-navbar {
  display: flex;
  position: absolute;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 99;
  width: 100%;
  top: 100%;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
  background: $primaryDark;
  overflow: hidden;
  max-height: 0;
  transition: max-height 0.25s ease-out;

  &.showNavBar {
    max-height: 500px;
    transition: max-height 0.3s ease-in;
  }

  a {
    padding: 12px 24px;
    font-weight: 600;

    .active-icon {
      margin-right: 4px;
      display: none;

      &.active {
        display: inline;
      }
    }
  }
}

@media only screen and (min-width: $SMALL_DISPLAY_SIZE) {
  .condensed-navbar {
    display: none;
  }
}

</style>
