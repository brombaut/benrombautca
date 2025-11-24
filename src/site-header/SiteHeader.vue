<template>
  <header id="site-header" class="header-bright">
    <div class="banner">
      <h1><b>Ben Rombaut</b></h1>
      <h4><i>Software Engineering Researcher</i></h4>
      <div id="external-profiles-container">
        <ExternalProfileIcon
          v-for="ep in externalProfiles"
          :key="ep.id()"
          :profile="ep"/>
      </div>
    </div>
    <NewNavBar/>
  </header>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import NewNavBar from "@/site-header/NewNavBar.vue";
import ExternalProfileIcon from "@/site-header/ExternalProfileIcon.vue";
import ExternalProfile from "./external-profile";

export default defineComponent({
  name: "SiteHeader",
  components: {
    NewNavBar,
    ExternalProfileIcon,
  },
  data() {
    const externalProfiles: ExternalProfile[] = [
      new ExternalProfile("LinkedIn", ["fab", "linkedin"], "https://www.linkedin.com/in/benjamin-rombaut/"),
      new ExternalProfile("GitHub", ["fab", "github"], "https://github.com/brombaut"),
      new ExternalProfile("Scholar", ["fab", "google-scholar"], "https://scholar.google.ca/citations?user=hBX9eycAAAAJ&hl=en"),
    ];
    return {
      externalProfiles,
    };
  },
  methods: {
    addBottomMargin(): void {
      this.$el.classList.add("bottom-margin");
    },
    removeBottomMargin(): void {
      this.$el.classList.remove("bottom-margin");
    },
  },
});
</script>

<style lang="scss">

.bottom-margin {
  margin-bottom: 42px; // Hight of the navbar - TODO: Change this to query the nav height and set the bottom maring style
}
#site-header {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;

  .banner {
    padding: 24px 0 12px 0px;
  }

  h1 {
    margin: 8px 0;
    font-size: 2em;
  }

  h4 {
    margin: 4px 0;
  }

  #external-profiles-container {
    display: flex;
    justify-content: center;
    margin-top: 8px;
  }

  @media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
    .banner {
      padding: 16px 0;
    }

    h4 {
      font-size: 0.8rem;
    }

    #external-profiles-container {
      margin-top: 12px;
    }
  }
}
</style>
