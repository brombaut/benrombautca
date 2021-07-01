<template>
  <nav class="full-navbar">
    <span class='active-route-highlight' ref="activeRouteHighlight"></span>
    <a class="about-me-nav" ref="aboutMeNav" @click="navigate('/about-me', 'aboutMeNav')">
      <span>About Me</span>
      <span class="underline"></span>
    </a>
    <a class="bookshelf-nav" ref="bookshelfNav" @click="navigate('/bookshelf', 'bookshelfNav')">
      <span>Bookshelf</span>
      <span class="underline"></span>
    </a>
    <a class="articles-nav" ref="articlesNav" @click="navigate('/articles', 'articlesNav')">
      <span>Articles</span>
      <span class="underline"></span>
    </a>
    <a class="software-nav" ref="softwareNav"  @click="navigate('/software', 'softwareNav')">
      <span>Software</span>
      <span class="underline"></span>
    </a>
  </nav>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class FullNavBar extends Vue {

  private navigate(routeName: string, refName: string): void {
    if (routeName !== this.$route.path) {
      this.$router.push(routeName);
      this.updateHighlight(refName);
    }
  }

  private updateHighlight(refName: string): void {
    const highlight: HTMLSpanElement = this.$refs.activeRouteHighlight as HTMLSpanElement;
    if (!highlight) return;
    const navAEl: HTMLAnchorElement = this.$refs[refName] as HTMLAnchorElement;
    if (!navAEl) return;
    const navBarEl: HTMLElement = navAEl.parentElement as HTMLElement;
    const navAElCoords = navAEl.getBoundingClientRect();
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
  }

  private firstHighlightDraw() {
    let currRouteName: string = this.$route.name || "";
    if (currRouteName) {
      if (currRouteName === "selectedArticle") {
        currRouteName = "articles";
      }
      if (currRouteName === "selectedSoftware") {
        currRouteName = "software";
      }
      const navEl: string = `${currRouteName}Nav`;
      this.updateHighlight(navEl);
      this.$nextTick(this.addTransitionToHighlight);
    }
  }

  private addTransitionToHighlight(): void {
    const highlight: HTMLSpanElement = this.$refs.activeRouteHighlight as HTMLSpanElement;
    if (!highlight) return;
    highlight.style.transition = "all 0.2s";
  }

  mounted() {
    this.firstHighlightDraw();
  }

}
</script>

<style lang="scss">
.full-navbar {
  display: flex;
  align-items: center;
  position: relative;

  .active-route-highlight {
    position: absolute;
    top: 0;
    background: $primary;
    left: 0;
    z-index: -1;
    display: block;
  }

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

@media only screen and (max-width: 640px) {
  .full-navbar {
    display: none;
  }
}
</style>
