<template>
  <section id="landing">
    <header>
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
import { Component, Vue } from "vue-property-decorator";

@Component
export default class LandingSection extends Vue {
  private externalProfiles: { [key: string]: string } = {
    linkedin: "https://www.linkedin.com/in/benjamin-rombaut/",
    github: "https://github.com/brombaut"
  };

  handleExternalProfileClicked(key: string) {
    const url = this.externalProfiles[key];
    if (url) {
      const result: Window | null = window.open(url, "_blank");
      if (result) {
        result.focus();
      }
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
    animation: slideUp 0.7s ease-out forwards;
    animation-delay: 0.5s;
    opacity: 0;
    position: relative;
    box-shadow: 0 2.8px 2.2px rgba(0, 0, 0, 0.034),
      0 6.7px 5.3px rgba(0, 0, 0, 0.048), 0 8.5px 10px rgba(0, 0, 0, 0.06),
      0 12.3px 7.9px rgba(0, 0, 0, 0.072), 0 21.8px 33.4px rgba(0, 0, 0, 0.086);
    // 0 30px 40px rgba(0, 0, 0, 0.12);

    h1 {
      font-size: 3.5rem;
    }

    h4 {
      font-size: 2rem;
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

  @keyframes slideUp {
    from {
      transform: translateY(20%);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
}
</style>
