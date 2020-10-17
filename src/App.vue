<template>
  <div id="app">
    <SiteHeader @routeClicked="hamdleRouteClickEvent"/>
    <main>
      <router-view />
    </main>
    <SiteFooter />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { bus } from "@/main";
import SiteFooter from "@/footer/SiteFooter.vue";
import SiteHeader from "@/site-header/SiteHeader.vue";
import CachedBookshelf from "@/bookshelf/cached-bookshelf";
import BookDataFetcher from "./bookshelf/book-data-fetcher";
import GoodreadsApiFetcher from "./bookshelf/goodreads-api-fetcher";
import BookDataParser from "./bookshelf/book-data-parser";
import BookXmlParser from "./bookshelf/book-xml-parser";
import BookshelfBuilder from "./bookshelf/bookshelf-builder";
import Bookshelf from "./bookshelf/bookshelf";
import UIUtils from "./utils/ui-utils";

interface PercentVisible {
  section: string;
  percentVisible: number;
}

@Component({
  components: {
    SiteFooter,
    SiteHeader,
  },
})
export default class App extends Vue {

  private initBookshelfCache() {
    const cachedBookshelf: CachedBookshelf = CachedBookshelf.getInstance();
  }

  private hamdleRouteClickEvent() {
    console.log("ROUTE CLICKED");
  }

  get curRoute(): string {
    return this.$route.name || "";
  }

  getElToScrollTo(): HTMLElement | null {
    let result: HTMLElement | null;
    switch (this.curRoute) {
    case "work": {
      result = document.querySelector("#work");
      break;
    }
    case "education": {
      result = document.querySelector("#education");
      break;
    }
    default: {
      result = document.querySelector("#site-header");
    }
    }
    return result;
  }

  scrollToRouteElement(): void {
    const elToScrollTo: HTMLElement | null = this.getElToScrollTo();
    console.log(elToScrollTo);
    if (elToScrollTo) {
      elToScrollTo.scrollIntoView({ behavior: "smooth" });
    } else {
      Vue.nextTick().then(() => {
        this.scrollToRouteElement();
      });
    }
  }

  private setCorrectNavElements(): void {
    const result: string[] = [];
    const orderedMostVisibleSections: PercentVisible[] = UIUtils.getSectionsPercentVisible();
    if (orderedMostVisibleSections[0].percentVisible < 0.1) {
      return;
    }
    result.push(orderedMostVisibleSections[0].section);
    const mostVisibleIsWorkOrEdu = orderedMostVisibleSections[0]?.section === "work"
      || orderedMostVisibleSections[0]?.section === "education";
    const secondMostVisibleIsWorkOrEdu = orderedMostVisibleSections[1]?.section === "work"
      || orderedMostVisibleSections[1]?.section === "education";
    if (mostVisibleIsWorkOrEdu && secondMostVisibleIsWorkOrEdu) {
      if (orderedMostVisibleSections[1]?.percentVisible > 0.5) {
        result.push(orderedMostVisibleSections[1].section);
      }
    }
    if (this.curRoute !== result[0]) {
      this.$router.push(result[0]);
    }
  }

  private handleScrollEvent(): void {
    this.setCorrectNavElements();
  }

  mounted() {
    this.initBookshelfCache();
    bus.$on("routeClicked", this.scrollToRouteElement);
    window.addEventListener("scroll", this.handleScrollEvent);
  }
}
</script>

<style lang="scss">
html,
body {
  margin: 0;
  background: $secondary;
  min-height: 100vh;
}
h1,h2,h3,h4,h5,h6 {
  margin: 0;
}

#app {
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $pFontColor;
  background: $secondary;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  overflow-y: auto;
  overflow-x: auto;
  position: relative;
  min-height: 100vh;

  main {
    flex: 1;
  }

  section {
    max-width: 1100px;
    margin: 16px 0;
    padding: 16px;
    z-index: 2;
    background: $secondaryLight;
    border-radius: 4px;
    box-shadow: 1px 1px 5px $pFontColor;
  }
}
</style>
