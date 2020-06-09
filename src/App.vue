<template>
  <div id="app">
    <NavBar />
    <main>
      <router-view />
    </main>
    <SiteFooter />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SiteFooter from "@/footer/SiteFooter.vue";
import NavBar from "@/navigation/NavBar.vue";
import CachedBookshelf from "@/bookshelf/cached-bookshelf";
import BookDataFetcher from "./bookshelf/book-data-fetcher";
import GoodreadsApiFetcher from "./bookshelf/goodreads-api-fetcher";
import BookDataParser from "./bookshelf/book-data-parser";
import BookXmlParser from "./bookshelf/book-xml-parser";
import BookshelfBuilder from "./bookshelf/bookshelf-builder";
import Bookshelf from "./bookshelf/bookshelf";

@Component({
  components: {
    SiteFooter,
    NavBar
  }
})
export default class App extends Vue {
  private initCaches() {
    this.initBookshelfCache();
  }

  private initBookshelfCache() {
    const cachedBookshelf: CachedBookshelf = CachedBookshelf.getInstance();
  }

  mounted() {
    this.initCaches();
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

#app {
  font-family: League Spartan, Helvetica, Arial, sans-serif;
  font-family: "Share Tech Mono", Helvetica, Arial, sans-serif;
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
    width: calc(100% - 16px);
    max-width: 1200px;
    padding: 48px 8px;
    z-index: 2;
  }
}
</style>
