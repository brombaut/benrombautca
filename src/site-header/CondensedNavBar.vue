<template>
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
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class CondensedNavBar extends Vue {

  @Prop()
  private mobileNavbarVisible!: boolean;

  private navigateMobile(routeName: string): void {
    this.$emit("closeMobileNavBar");
    this.navigate(routeName);
  }

  private navigate(routeName: string): void {
    if (routeName !== this.$route.path) {
      this.$router.push(routeName);
    }
  }
}
</script>

<style lang="scss">
.condensed-navbar {
  display: none;
  position: absolute;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  padding: 0px 16px;
  z-index: 99;
  width: 100%;
  top: 100%;
  flex-direction: column;
  align-items: flex-start;
  background: $primaryDark;

  &.showNavBar {
    display: flex;
  }

  a {
    padding: 12px 8px;
    font-weight: bold;
    width: 100%;
    border-bottom: 1px solid $primaryDarkest;
    border-top: 1px solid $primaryDarkest;
  }
}

</style>
