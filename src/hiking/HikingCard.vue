<template>
  <div class="hike-card">
    <div class="hike-info">
      <h3 class="header">{{ hike.name }}</h3>
      <div class="body">
        <div class="wrapper">
          <div class="label">Hike Date:</div>
          <div class="value">{{ hikeDate }}</div>
        </div>
        <div class="wrapper">
          <div class="label">Location:</div>
          <div class="value">{{ hike.location }}</div>
        </div>
        <div v-html="hike.description" />
      </div>
    </div>
    <div class="hike-images">
      <ImageCarousel :images="hike.images" />
    </div>
  </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import ImageCarousel from "@/shared/ImageCarousel.vue";
import { Hike } from "./types";

export default defineComponent({
  name: "HikingCard",
  components: {
    ImageCarousel,
  },
  props: {
    hike: {
      type: Object as PropType<Hike>,
      required: true,
    },
  },
  computed: {
    hikeDate(): string {
      if (this.hike.date instanceof Date) {
        const d: Date = this.hike.date;
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
      }
      return this.hike.date;

    },
  },
});
</script>

<style lang="scss">
.hike-card {
  display: flex;
  flex-direction: row;
  width: 100%;
  border-top: 2px solid $primaryDark;
  padding-top: 16px;

  @media only screen and (max-width: $MAX_SECTION_SIZE) {
    flex-direction: column;
  }

  .hike-info {
    flex: 1;
    // margin: 0 8px 8px 8px;
    padding: 0 4px;

    .header {
      color: $primary;
    }

    .body {
      margin-left: 20px;

      @media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
        font-size: 0.8em;
      }

      .wrapper {
        display: flex;
        margin: 8px 0;

        .label {
          margin-right: 4px;
          // color: $primaryDark;
          font-weight: 600;
        }

        .value {
          // font-weight: bold;

          a {
            cursor: pointer;
            text-decoration: underline;

            &:hover {
              color:$primaryDark;
            }
          }
        }
      }
    }
  }

  .hike-images {
    flex: 1;
  }
}

</style>
