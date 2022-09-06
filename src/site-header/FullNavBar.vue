<template>
  <nav class="full-navbar">
    <BackButton />
    <div class="nav-items">
      <span class='active-route-highlight' ref="activeRouteHighlight"></span>
      <FullNavItem ref="aboutMeNav" route="/about-me" text="About Me" @clicked="updateHighlight" />
      <FullNavItem ref="publicationsNav" route="/publications" text="Publications" @clicked="updateHighlight" />
      <FullNavItem ref="bookshelfNav" route="/bookshelf" text="Bookshelf" @clicked="updateHighlight" />
      <FullNavItem ref="articlesNav" route="/articles" text="Articles" @clicked="updateHighlight" />
      <FullNavItem ref="softwareNav" route="/software" text="Software" @clicked="updateHighlight" />
      <FullNavItem ref="runningNav" route="/running" text="Running" @clicked="updateHighlight" />
    </div>
  </nav>
</template>

<script lang="ts">
import Vue from "vue";
import FullNavItem from "./FullNavItem.vue";
import BackButton from "./BackButton.vue";
import appConfig from "@/app_config";

export default Vue.extend({
  name: "FullNavBar",
  components: {
    FullNavItem,
    BackButton,
  },
  data() {
    const showMarathons = appConfig.flagMarathons;
    return {
      showMarathons,
    };
  },
  methods: {
    updateHighlight(navItemEl: HTMLAnchorElement): void {
      const highlight: HTMLSpanElement = this.$refs.activeRouteHighlight as HTMLSpanElement;
      if (!highlight) return;
      const navBarEl: HTMLElement = navItemEl.parentElement as HTMLElement;
      const navAElCoords = navItemEl.getBoundingClientRect();
      const navBarCoords = navBarEl.getBoundingClientRect();
      const coords = {
        width: navAElCoords.width,
        height: navBarCoords.height - 0,
        top: 0,
        left: navAElCoords.left - navBarCoords.left,
      };
      highlight.style.width = `${coords.width}px`;
      highlight.style.height = `${coords.height}px`;

      highlight.style.transform = `translate(${coords.left}px, ${coords.top}px)`;
    },
    getActiveRouteNavElRef(): string {
      let currRouteName: string = this.$route.name || "";
      if (!currRouteName) return "";
      if (currRouteName === "land") currRouteName = "aboutMe";
      if (currRouteName === "selectedArticle") currRouteName = "articles";
      if (currRouteName === "selectedSoftware") currRouteName = "software";
      const navEl: string = `${currRouteName}Nav`;
      return navEl;
    },
    getNavElFromRef(ref: string): HTMLAnchorElement {
      const fromRefs = this.$refs[ref] as Vue;
      const activeNavEl: HTMLAnchorElement = fromRefs.$el as HTMLAnchorElement;
      return activeNavEl;
    },
    addTransitionToHighlight(): void {
      const highlight: HTMLSpanElement = this.$refs.activeRouteHighlight as HTMLSpanElement;
      if (!highlight) return;
      highlight.style.transition = "all 0.2s";
    },
    removeTransitionFromHighlight(): void {
      const highlight: HTMLSpanElement = this.$refs.activeRouteHighlight as HTMLSpanElement;
      if (!highlight) return;
      highlight.style.transition = "";
    },
    redrawHighlight(): void {
      const activeRef = this.getActiveRouteNavElRef();
      if (!activeRef) return;
      const activeNavEl = this.getNavElFromRef(activeRef);
      if (!activeNavEl) return;
      this.removeTransitionFromHighlight();
      this.updateHighlight(activeNavEl);
      this.$nextTick(this.addTransitionToHighlight);
    },
  },
  mounted() {
    this.redrawHighlight();
    window.addEventListener("resize", this.redrawHighlight);
  },
});
</script>

<style lang="scss">
.full-navbar {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  max-width: 1100px;
  position: relative;

  .nav-items {
    position: relative;
    display: flex;
    flex-direction: row;
  }

  .active-route-highlight {
    position: absolute;
    top: 0;
    background: $primary;
    left: 0;
    z-index: -1;
    display: block;
  }
}

@media only screen and (max-width: $PHONE_DISPLAY_SIZE) {
  .full-navbar {
    display: none;
  }
}
</style>
