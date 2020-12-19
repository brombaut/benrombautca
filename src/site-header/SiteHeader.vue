<template>
  <header id="site-header" class="header-bright">
    <div class="banner">
      <h1><b>BEN ROMBAUT</b></h1>
      <h4><i>Master of Science Candidate at the Software Analysis & Intelligence Lab, Queen's University</i></h4>
      <div id="external-profiles-container">
        <ExternalProfileIcon
          v-for="ep in externalProfiles"
          :key="ep.id()"
          :profile="ep"/>
      </div>
    </div>
    <NavBar />
  </header>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NavBar from "@/site-header/NavBar.vue";
import ExternalProfileIcon from "@/site-header/ExternalProfileIcon.vue";
import ExternalProfile from "./external-profile";

@Component({
  components: {
    NavBar,
    ExternalProfileIcon,
  },
})
export default class SiteHeader extends Vue {
  private externalProfileUrls: { [key: string]: string } = {
    linkedin: "https://www.linkedin.com/in/benjamin-rombaut/",
    github: "https://github.com/brombaut",
    dev: "https://dev.to/brombaut",
    stackoverflow: "https://stackoverflow.com/users/5816686/ben",
  };

  private externalProfiles: ExternalProfile[] = [
    new ExternalProfile("github", ["fab", "github"], this.externalProfileUrls.github),
    new ExternalProfile("linkedin", ["fab", "linkedin"], this.externalProfileUrls.linkedin),
    new ExternalProfile("dev", ["fab", "dev"], this.externalProfileUrls.dev),
    new ExternalProfile("stackoverflow", ["fab", "stack-overflow"], this.externalProfileUrls.stackoverflow),
  ]

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
  align-items: center;

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
    margin-top: 16px;
    display: flex;
    justify-content: center;
  }

  @media only screen and (max-width: 640px) {
    .banner {
      padding: 16px 0;
    }
    h1 {
      font-size: 2.5rem;
    }

    h4 {
      font-size: 0.8rem;
    }

    #external-profiles-container {
      margin-top: 20px;
      // TODO: Confirm mobile works as expected
      a {
        margin: 0 20px;
        font-size: 1.5rem;
      }
    }
  }
}
</style>
