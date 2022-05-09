<template>
  <div class="marathon-card">
    <div class="marathon-info">
      <h3 class="header"><a :href="marathon.link" target="_blank">{{ marathon.name }}</a></h3>
      <div class="body">
        <div class="wrapper">
           <div class="label">Race Date:</div>
           <div class="value">{{ marathonDate }}</div>
        </div>
        <div class="wrapper">
          <div class="label">Official Time:</div>
          <div class="value" v-html="marathon.runningTime"></div>
        </div>
        <div class="wrapper">
          <div class="label">Placement:</div>
          <div class="value" v-html="marathon.placement"></div>
        </div>
        <div v-html="marathon.description"></div>
      </div>
    </div>
    <div class="marathon-images">
      <ImageCarousel :images="marathon.images" />
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
  },
});
</script>

<style lang="scss">
.marathon-card {
  display: flex;
  flex-direction: row;
  width: 100%;

  @media only screen and (max-width: $MAX_SECTION_SIZE) {
    flex-direction: column;
  }

  .marathon-info {
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
          font-weight: bold;
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

  .marathon-images {
    flex: 1;
  }
}

</style>
