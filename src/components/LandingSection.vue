<template>
  <section id="landing">
    <header>
      <h1>BEN ROMBAUT</h1>
      <h4>Software Developer</h4>
    </header>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class LandingSection extends Vue {}
</script>

<style lang="scss">
#landing {
  padding: 0 0 !important;
  height: 100vh;
  display: flex;
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
      0 6.7px 5.3px rgba(0, 0, 0, 0.048),
      0 8.5px 10px rgba(0, 0, 0, 0.06),
      0 12.3px 7.9px rgba(0, 0, 0, 0.072),
      0 21.8px 33.4px rgba(0, 0, 0, 0.086);
      // 0 30px 40px rgba(0, 0, 0, 0.12);

    h1 {
      font-size: 3.5rem;
    }

    h4 {
      font-size: 2rem;
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
