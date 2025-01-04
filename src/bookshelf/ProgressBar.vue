<template>
  <div class="progress-bar">
    <div class='progress-bar-fill' ref='progressBarFill'></div>
    <div class='text' :class="{'add-padding': hidePercent}">
      {{ text }} <span>{{ numer }}</span>/<span>{{ denom }}</span> <span v-if="!hidePercent">({{ percentDone }}%)</span>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: "ProgressBar",
  props: {
    text: {
      type: String,
      required: true,
    },
    numer: {
      type: Number,
      required: true,
    },
    denom: {
      type: Number,
      required: true,
    },
    hidePercent: {
      type: Boolean,
      required: false,
    },
  },
  computed: {
    percentDone(): number {
      if (!this.numer) return 0;
      if (!this.denom) return 0;
      return Math.floor((this.numer / this.denom) * 100);
    },
  },
  methods: {
    setProgressBarFill() {
      const numerator = this.numer || 0;
      const denominator = this.denom || 1; // Prevent division by zero
      const fractionDone = numerator / denominator;
      const percentDone = Math.min(fractionDone * 100, 100); // Cap at 100%
      const progressBarEl = this.$refs.progressBarFill as HTMLDivElement;
      progressBarEl.style.width = `${percentDone}%`;
    },
  },
  mounted() {
    this.setProgressBarFill();
  },
});
</script>

<style lang="scss">

.progress-bar {
  background-color: $primaryDark;
  border-radius: 4px;
  padding: 6px 4px;
  position: relative;
  z-index: 0;
  width: calc(100% - 40px);
  // max-width: 164px;

  .text {
    font-size: 0.8em;
    color: white;
    z-index: 2;
    position: relative;

    &.add-padding {
      padding-left: 4px;
      padding-right: 8px;
    }
  }

  .progress-bar-fill {
    position: absolute;
    top: 0;
    left: 0;
    background-color: $primary;
    height: 100%;
    width: 50%;
    border-radius: 4px;
    z-index: 1;
  }
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .progress-bar{
    font-size: 0.8em;
  }
}

@media only screen and (max-width: $PHONE_DISPLAY_SIZE) {
  .progress-bar{
    font-size: 0.4em; // idk if this is doing anything
    width: calc(100% - 20px);
  }
}

</style>
