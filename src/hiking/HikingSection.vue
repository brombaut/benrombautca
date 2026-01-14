<template>
  <section id="hikes">
    <SectionHeader
      title="Hiking"
      icon="hiking"
      subtext="Some of the hikes I've done over the years." />

    <!-- Adirondack 46er Goal -->
    <div class="hiking-goal">
      <h3>Adirondack 46er Goal</h3>
      <p>Working towards summiting all 46 of the 4,000+ foot peaks in the Adirondacks.</p>
      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
        <span class="progress-text">{{ completedPeaks }} / {{ totalPeaks }} peaks</span>
      </div>
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
      completedPeaks: 5,
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

  .hiking-goal {
    margin: 1.5rem 0;
    padding: 1.5rem;
    background: rgba(51, 129, 219, 0.05);
    border-radius: 8px;
    border-left: 4px solid $primary;
    box-sizing: border-box;

    h3 {
      margin: 0 0 0.5rem 0;
      color: $primary;
      font-size: 1.3rem;
      font-weight: 600;
    }

    p {
      margin: 0 0 1rem 0;
      color: $fontColor;
      line-height: 1.5;
    }

    .progress-bar-container {
      position: relative;
      height: 30px;
      background: rgba(0, 0, 0, 0.1);
      border-radius: 15px;
      overflow: hidden;

      .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, $primary 0%, $primaryDark 100%);
        transition: width 0.3s ease;
        border-radius: 15px;
      }

      .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: $fontColor;
        font-weight: 600;
        font-size: 0.9rem;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
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
