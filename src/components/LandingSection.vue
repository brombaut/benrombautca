<template>
  <section id="landing">
    <header ref="header" @click="handleHeaderClicked()">
      <h1>BEN ROMBAUT</h1>
      <h4>Software Developer</h4>
    </header>
    <div id="external-profiles-container">
      <a id="linkedin-link" :href="externalProfiles['linkedin']">
        <font-awesome-icon
          id="linkedin-icon"
          class="icon"
          @click.stop.prevent="handleExternalProfileClicked('linkedin')"
          :icon="['fab', 'linkedin']"
        />
      </a>
      <a id="github-link" :href="externalProfiles['github']">
        <font-awesome-icon
          id="github-icon"
          class="icon"
          @click.stop.prevent="handleExternalProfileClicked('github')"
          :icon="['fab', 'github']"
        />
      </a>
    </div>
  </section>
</template>

<script lang="ts">
import {
  Component, Vue, Prop, Watch
} from "vue-property-decorator";

@Component
export default class LandingSection extends Vue {
  private externalProfiles: { [key: string]: string } = {
    linkedin: "https://www.linkedin.com/in/benjamin-rombaut/",
    github: "https://github.com/brombaut"
  };

  private mainHeader!: HTMLHeadingElement;

  @Prop()
  mouseTrailerVisible!: boolean;

  mounted() {
    this.mainHeader = this.$refs.header as HTMLHeadingElement;
    this.mainHeader.classList.add("slide-in");
  }

  handleHeaderClicked() {
    this.$emit("headerClicked");
  }

  handleExternalProfileClicked(key: string) {
    const url = this.externalProfiles[key];
    if (url) {
      const result: Window | null = window.open(url, "_blank");
      if (result) {
        result.focus();
      }
    }
  }

  @Watch("mouseTrailerVisible")
  setMainHeaderAnimation() {
    this.mainHeader.classList.remove("slide-in");
    if (this.mouseTrailerVisible) {
      this.mainHeader.classList.add("drawing-active");
    } else {
      this.mainHeader.classList.remove("drawing-active");
    }
  }
}
</script>

<style lang="scss">
#landing {
  padding: 0 0 !important;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  header {
    background: $primaryDark;
    padding: 80px;
    border-radius: 50%;
    position: relative;
    transition: 0.3s all;
    box-shadow: 0 2.8px 2.2px rgba(0, 0, 0, 0.034),
      0 6.7px 5.3px rgba(0, 0, 0, 0.048), 0 8.5px 10px rgba(0, 0, 0, 0.06),
      0 12.3px 7.9px rgba(0, 0, 0, 0.072), 0 21.8px 33.4px rgba(0, 0, 0, 0.086);

    h1 {
      font-size: 3.5rem;
    }

    h4 {
      font-size: 2rem;
    }

    &.slide-in {
      animation: slideUp 0.7s ease-out forwards;
      animation-delay: 0.5s;
      opacity: 0;
    }

    &.drawing-active {
      animation: pulse 4s ease infinite;
    }

    &:hover {
      cursor: pointer;
      box-shadow: 0 0 2.2px rgba(51, 129, 219, 0.134),
        0 0 5.3px rgba(51, 129, 219, 0.148), 0 0 10px rgba(51, 129, 219, 0.16),
        0 0 7.9px rgba(51, 129, 219, 0.172),
        0 0 33.4px rgba(51, 129, 219, 0.186);
    }
  }

  #external-profiles-container {
    margin-top: 32px;

    a {
      margin: 0 20px;
      font-size: 2rem;
      color: $primary;
      transition: 0.3s color;
      animation: slideUp 0.7s ease-out forwards;
      animation-delay: 0.5s;

      &:hover {
        color: white;
        cursor: pointer;
      }
    }

    .icon {
      animation: slideUp 0.7s ease-out forwards;
      opacity: 0;
    }

    #linkedin-icon {
      animation-delay: 1s;
    }
    #github-icon {
      animation-delay: 1.5s;
    }
  }
}
</style>
