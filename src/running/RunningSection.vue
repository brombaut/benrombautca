<template>
  <section id="races">
    <SectionHeader
      title="Running"
      icon="running"
      subtext="I got into running while the pandemic had the gyms closed. Now I'd like to make a habit of running a different marathon every few years, with some other races every now and then. I ran my first official marathon in the Spring of 2022, which is listed below. Hopefully I'll add more to this list in the coming years." />
    <!-- Upcoming Races -->
    <div class="upcoming-races">
      <h3>Upcoming Races</h3>
      <ul>
        <li>
          <a
            href="https://www.jecoursqc.com/en/beneva-quebec-city-marathon-presented-by-montellier/races/#/21-1k-shop-sante-presented-by-wknd-91-9"
            target="_blank"
            rel="noopener noreferrer">
            Quebec City Half Marathon
          </a>
          - Beneva Quebec City Marathon, Fall 2026 (Oct 5)
        </li>
      </ul>
    </div>

    <div class="section-body">
      <RunningCard
        v-for="race in orderedRaces"
        :key="race.name"
        :race="race" />
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import RunningCard from "./RunningCard.vue";
import races from "./races";
import { Race } from "./types";

export default defineComponent({
  name: "RunningSection",
  components: {
    SectionHeader,
    RunningCard,
  },
  data() {
    return {
      races,
    };
  },
  computed: {
    orderedRaces(): Race[] {
      return [...this.races].sort((a: Race, b: Race) => {
        return b.orderDate.getTime() - a.orderDate.getTime();
      });
    },
  },
});
</script>

<style lang="scss">
#races {
  display: flex;
  flex-direction: column;

  .upcoming-races {
    margin: 1.5rem 0;
    padding: 1.5rem;
    background: rgba(51, 129, 219, 0.05);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    box-sizing: border-box;

    h3 {
      margin: 0 0 0.75rem 0;
      color: $primary;
      font-size: 1.3rem;
      font-weight: 600;
    }

    ul {
      margin: 0;
      padding-left: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }

    li {
      color: $fontColor;
      line-height: 1.5;
    }

    a {
      color: $primary;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
