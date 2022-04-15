<template>
  <div class="marathon-card">
    <div class="marathon-info">
      <h3 class="header"><a :href="marathon.link" target="_blank">{{ marathon.name }}</a></h3>
      <div class="body">
        <div class="wrapper">
           <div>Race Date:&nbsp;</div><div>{{ marathonDate }}</div>
        </div>
        <div class="wrapper">
          <div>Official Time:&nbsp;</div><div>{{ marathon.runningTime }}</div>
        </div>
        <div v-html="marathon.description"></div>
      </div>
    </div>
    <div class="marathon-images">
      <ImageCarousel :images="imageSources" />
      <!-- <img :src="imageSource" :alt="marathon.images[0]" /> -->
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import ImageCarousel from "./ImageCarousel.vue";
import { Marathon } from "./types";

export default Vue.extend({
  name: "MarathonCard",
  components: {
    ImageCarousel,
  },
  props: {
    marathon: {
      type: Object as PropType<Marathon>,
      required: true,
    },
  },
  computed: {
    marathonDate() {
      const d: Date = this.marathon.date;
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
    },
    imageSource(): string {
      return `marathon-images/${this.marathon.images[0]}`;
    },
    imageSources(): String[] {
      return this.marathon.images.map((i => `marathon-images/${i}`));
    },
  },
});
</script>

<style lang="scss">
.marathon-card {
  display: flex;
  flex-direction: row;
  width: 100%;

  @media only screen and (max-width: $MEDIUM_DISPLAY_SIZE) {
    flex-direction: column;
  }

  .marathon-info {
    flex: 1;
    margin: 0 8px 8px 8px;

    .header {
      color: $primary;
    }

    .body {
      margin-left: 20px;

      .wrapper {
        display: flex;
        margin: 8px 0;
      }
    }
  }

  .marathon-images {
    flex: 1;

    img {
      width: 100%;
    }
  }
}

</style>
