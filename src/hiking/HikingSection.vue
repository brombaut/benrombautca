<template>
  <section id="hikes">
    <SectionHeader
      title="Hiking"
      icon="hiking"
      subtext="Some of the hikes I've done over the years." />
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
  },
});
</script>

<style lang="scss">
#hikes {
  display: flex;
  flex-direction: column;

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
