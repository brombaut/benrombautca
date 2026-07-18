<template>
  <section id="hikes">
    <SectionHeader
      title="Hiking"
      icon="hiking"
      subtext="Some of the hikes I've done over the years." />

    <!-- Highlights -->
    <div class="hiking-highlights">
      <h3>Highlights</h3>
      <ul>
        <li>
          Summited Mount Kilimanjaro via the Lemosho route, 7 days to reach 19,341 feet,
          the highest point on the African continent. An incredible experience!
        </li>
        <li>
          A multi-week east-to-west coast road trip with my sister through national parks across
          the northern US, including Maquoketa Caves, Badlands, Grand Teton, Yellowstone, Glacier,
          and Mount Rainier, before finishing with hiking in British Columbia and driving back
          through Canada.
        </li>
        <li>
          Working towards completing all 46 Adirondack High Peaks (the "46ers"),
          the 46 mountains in the Adirondacks over 4,000 feet.
          <div class="progress-bar-container">
            <div class="progress-bar" :style="{ width: `${progressPercentage}%` }" />
            <span class="progress-text">{{ completedPeaks }} / {{ totalPeaks }} peaks</span>
          </div>
        </li>
      </ul>
    </div>

    <div class="section-body">
      <HikingCard
        v-for="hike in orderedHikes"
        :key="new Date(hike.date).getTime()"
        :hike="hike" />

      <!-- Show More button -->
      <button
        v-if="currentMax < hikes.length"
        type="button"
        class="show-more"
        @click="showMore">
        Show more
      </button>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import HikingCard from "./HikingCard.vue";
import hikes from "./hikes";
import { Hike } from "./types";

export default defineComponent({
  name: "HikingSection",
  components: {
    SectionHeader,
    HikingCard,
  },
  props: {
    maxHikes: {
      type: Number,
      default: 10,
    },
  },
  data() {
    return {
      hikes,
      // initialize a mutable currentMax from the prop so we can extend it
      currentMax: (this as any).maxHikes,
      // Adirondack 46er tracking
      completedPeaks: 14,
      totalPeaks: 46,
    };
  },
  watch: {
    // if parent updates the prop, reset the currentMax
    maxHikes(newVal: number) {
      (this as any).currentMax = newVal;
    },
  },
  methods: {
    showMore() {
      (this as any).currentMax = Math.min((this as any).currentMax + 10, this.hikes.length);
    },
  },
  computed: {
    orderedHikes(): Hike[] {
      return [...this.hikes]
        .sort((a: Hike, b: Hike) => b.orderDate.getTime() - a.orderDate.getTime())
        .slice(0, (this as any).currentMax);
    },
    progressPercentage(): number {
      return Math.round((this.completedPeaks / this.totalPeaks) * 100);
    },
  },
});
</script>

<style lang="scss">
#hikes {
  display: flex;
  flex-direction: column;

  .hiking-highlights {
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

    .progress-bar-container {
      position: relative;
      height: 18px;
      margin-top: 0.5rem;
      max-width: 320px;
      background: rgba(0, 0, 0, 0.1);
      border-radius: 9px;
      overflow: hidden;

      .progress-bar {
        height: 100%;
        background: $primary;
        border-radius: 9px;
      }

      .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: $fontColor;
        font-weight: 600;
        font-size: 0.75rem;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
        white-space: nowrap;
      }
    }
  }

  .section-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .show-more {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: $primary;
    color: $fontColorInverted;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    align-self: center;
    box-shadow: 0 2px 6px rgba(51, 129, 219, 0.12);
    transition: background 0.18s ease, transform 0.08s ease, box-shadow 0.18s ease;
    font-weight: 600;
    font-size: 1.05rem;

    &:hover {
      background: $primaryDark;
      box-shadow: 0 4px 10px rgba(51, 129, 219, 0.16);
    }

    &:active {
      transform: translateY(1px) scale(0.998);
    }

    &:focus {
      outline: 2px solid rgba(0,0,0,0.06);
      outline-offset: 2px;
    }
  }
}
</style>
