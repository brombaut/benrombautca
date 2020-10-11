<template>
  <header id="site-header" class="header-bright">
    <div class="banner">
      <h1><b>BEN ROMBAUT</b></h1>
      <h4><i>Master of Science Candidate at the Software Analysis & Intelligence Lab, Queen's University</i></h4>
      <div id="external-profiles-container">
        <a id="github-link" :href="externalProfiles['github']">
          <font-awesome-icon
            id="github-icon"
            class="icon"
            @click.stop.prevent="handleExternalProfileClicked('github')"
            :icon="['fab', 'github']"
          />
        </a>
        <a id="linkedin-link" :href="externalProfiles['linkedin']">
          <font-awesome-icon
            id="linkedin-icon"
            class="icon"
            @click.stop.prevent="handleExternalProfileClicked('linkedin')"
            :icon="['fab', 'linkedin']"
          />
        </a>
      </div>
    </div>
    <NavBar />
  </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NavBar from "@/site-header/NavBar.vue";

@Component({
  components: {
    NavBar,
  },
})
export default class SiteHeader extends Vue {
  private externalProfiles: { [key: string]: string } = {
    linkedin: "https://www.linkedin.com/in/benjamin-rombaut/",
    github: "https://github.com/brombaut",
  };

  private handleExternalProfileClicked(key: string) {
    const url = this.externalProfiles[key];
    if (url) {
      const result: Window | null = window.open(url, "_blank");
      if (result) {
        result.focus();
      }
    }
  }

  public addBottomMargin(): void {
    this.$el.classList.add("bottom-margin");
  }

  public removeBottomMargin(): void {
    this.$el.classList.remove("bottom-margin");
  }
}
</script>

<style lang="scss">

.bottom-margin {
  margin-bottom: 56px;
}
#site-header {
  width: 100%;
  display: flex;
  flex-direction: column;

  .banner {
    padding: 32px 0;
  }

  h1 {
    margin: 8px 0;
    font-size: 3.5rem;
  }

  h4 {
    margin: 4px 0;
  }

  #external-profiles-container {
    margin-top: 32px;

    a {
      margin: 0 20px;
      font-size: 2rem;
      color: $secondary !important;

      .icon{
        color: inherit;
        transition: 0.3s;
      }

      &:hover {
        cursor: pointer;

        .icon {
          color: $primaryDarkest;
        }
      }
    }
  }
}
</style>
