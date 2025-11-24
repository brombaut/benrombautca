<template>
  <div class="race-card">
    <div class="race-info">
      <h3 class="header"><a :href="race.link" target="_blank">{{ race.name }}</a></h3>
      <div class="body">
        <div class="wrapper">
           <div class="label">Race Date:</div>
           <div class="value">{{ raceDate }}</div>
        </div>
        <div v-if="race.runningTime" class="wrapper">
          <div class="label">Official Time:</div>
          <div class="value" v-html="race.runningTime"></div>
        </div>
        <div v-if="race.placement" class="wrapper">
          <div class="label">Placement:</div>
          <div class="value" v-html="race.placement"></div>
        </div>
        <div v-html="race.description"></div>
      </div>
    </div>
    <div class="race-images">
      <ImageCarousel :images="race.images"/>
    </div>
  </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import ImageCarousel from "@/shared/ImageCarousel.vue";
import { Race } from "./types";

export default defineComponent({
  name: "RaceCard",
  components: {
    ImageCarousel,
  },
  props: {
    race: {
      type: Object as PropType<Race>,
      required: true,
    },
  },
  computed: {
    raceDate(): string {
      if (this.race.date instanceof Date) {
        const d: Date = this.race.date;
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
      } else {
        return this.race.date;
      }
    },
  },
});
</script>

<style lang="scss">
.race-card {
  display: flex;
  flex-direction: row;
  width: 100%;
  border-top: 2px solid $primaryDark;
  padding-top: 16px;

  @media only screen and (max-width: $MAX_SECTION_SIZE) {
    flex-direction: column;
  }

  .race-info {
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

  .race-images {
    flex: 1;
  }
}

</style>
