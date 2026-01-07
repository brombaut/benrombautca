<template>
  <nav class="condensed-navbar" ref="mobileNavbar" :class="{ showNavBar: mobileNavbarVisible }">
    <a tabindex="0" @click="navigateMobile('/about-me')" @keydown.enter="navigateMobile('/about-me')">
      <font-awesome-icon
        class='active-icon'
        :class="{ active: routeIsActive('aboutMe') }"
        :icon="['fas', 'chevron-right']" />
      <span>About Me</span>
    </a>
    <a tabindex="0" @click="navigateMobile('/publications')" @keydown.enter="navigateMobile('/publications')">
      <font-awesome-icon
        class='active-icon'
        :class="{ active: routeIsActive('publications') }"
        :icon="['fas', 'chevron-right']" />
      <span>Publications</span>
    </a>
    <a tabindex="0" @click="navigateMobile('/bookshelf')" @keydown.enter="navigateMobile('/bookshelf')">
      <font-awesome-icon
        class='active-icon'
        :class="{ active: routeIsActive('bookshelf') }"
        :icon="['fas', 'chevron-right']" />
      <span>Bookshelf</span>
    </a>
    <a tabindex="0" @click="navigateMobile('/articles')" @keydown.enter="navigateMobile('/articles')">
      <font-awesome-icon
        class='active-icon'
        :class="{ active: routeIsActive('articles') }"
        :icon="['fas', 'chevron-right']" />
      <span>Articles</span>
    </a>
    <!-- <a @click="navigateMobile('/software')">
      <font-awesome-icon
        class='active-icon'
        :class="{active: routeIsActive('software')}"
        :icon="['fas', 'chevron-right']"/>
      <span>Software</span>
    </a> -->
    <a tabindex="0" @click="navigateMobile('/running')" @keydown.enter="navigateMobile('/running')">
      <font-awesome-icon
        class='active-icon'
        :class="{ active: routeIsActive('running') }"
        :icon="['fas', 'chevron-right']" />
      <span>Running</span>
    </a>
    <a tabindex="0" @click="navigateMobile('/hiking')" @keydown.enter="navigateMobile('/hiking')">
      <font-awesome-icon
        class='active-icon'
        :class="{ active: routeIsActive('hiking') }"
        :icon="['fas', 'chevron-right']" />
      <span>Hiking</span>
    </a>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import appConfig from "@/app_config";

export default defineComponent({
  props: {
    mobileNavbarVisible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    const showMarathons = appConfig.flagMarathons;
    return {
      showMarathons,
    };
  },
  methods: {
    navigateMobile(routeName: string): void {
      this.$emit("closeMobileNavBar");
      this.navigate(routeName);
    },
    navigate(routeName: string): void {
      if (routeName !== this.$route.path) {
        this.$router.push(routeName);
      }
    },
    routeIsActive(routeName: string): boolean {
      switch (routeName) {
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
  display: none;
  position: absolute;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 99;
  width: 100%;
  top: 100%;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
  background: $primaryDark;

  &.showNavBar {
    display: flex;
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
  .condensed-navbar.showNavBar {
    display: none;
  }
}

</style>
