<template>
  <div class="about-me-extended">
    <AboutMeSection />
    <WorkEducationSection />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { bus } from "@/main";
import AboutMeSection from "@/aboutMe/AboutMeSection.vue";
import WorkEducationSection from "@/workEducation/WorkEducationSection.vue";

export default Vue.extend({
  name: "AboutMeExtended",
  components: {
    AboutMeSection,
    WorkEducationSection,
  },
  computed: {
    curRoute(): string {
      return this.$route.name || "";
    },
  },
  methods: {
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
    },
    scrollToRouteElement(): void {
      const elToScrollTo: HTMLElement | null = this.getElToScrollTo();
      if (elToScrollTo) {
        elToScrollTo.scrollIntoView({ behavior: "smooth" });
      }
    },
  },
  mounted() {
    setTimeout(this.scrollToRouteElement, 150);
    bus.$on("routeClicked", this.scrollToRouteElement);
  },
});

// @Component({
//   components: {
//     AboutMeSection,
//     WorkEducationSection,
//   },
// })
// export default class AboutMeExtended extends Vue {

//   get curRoute(): string {
//     return this.$route.name || "";
//   }

//   getElToScrollTo(): HTMLElement | null {
//     let result: HTMLElement | null;
//     switch (this.curRoute) {
//     case "work": {
//       result = document.querySelector("#work");
//       break;
//     }
//     case "education": {
//       result = document.querySelector("#education");
//       break;
//     }
//     default: {
//       result = document.querySelector("#site-header");
//     }
//     }
//     return result;
//   }

//   scrollToRouteElement(): void {
//     const elToScrollTo: HTMLElement | null = this.getElToScrollTo();
//     if (elToScrollTo) {
//       elToScrollTo.scrollIntoView({ behavior: "smooth" });
//     }
//   }

//   mounted() {
//     setTimeout(this.scrollToRouteElement, 150);
//     bus.$on("routeClicked", this.scrollToRouteElement);
//   }
// }
</script>

<style lang="scss">
.about-me-extended {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
</style>
