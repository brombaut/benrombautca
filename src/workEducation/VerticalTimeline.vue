<template>
  <div class="vertical-timeline">
    <SectionHeader :title="title" :icon="icon" />
    <div class="section-body">
      <div class="wrapper" ref="wrapper">
        <div class="vertical-line" ref="verticalLine" />
        <ul v-if="type === 'education'">
          <EducationCard
            v-for="education in entitiesToShow"
            :key="education.title"
            :education="education"
          />
        </ul>
        <ul v-else-if="type === 'work'">
          <WorkCard v-for="work in entitiesToShow" :key="work.title" :work="work" />
        </ul>
      </div>
    </div>
    <div v-if="showLimit && !showMore" class="show-more-wrapper">
      <div
        class="show-more"
        role="button"
        tabindex="0"
        @click="showMoreClicked()"
        @keydown.enter="showMoreClicked()">
        <font-awesome-icon :icon="['fas', 'caret-down']" />
        <span>SHOW MORE</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import EducationCard from "./EducationCard.vue";
import WorkCard from "./WorkCard.vue";
import { TimelineEntities } from "./timeline-entities";
import SectionHeader from "../shared/SectionHeader.vue";

export default defineComponent({
  name: "VerticalTimeline",
  components: {
    EducationCard,
    WorkCard,
    SectionHeader,
  },
  props: {
    type: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
    timelineEntities: {
      type: Array as PropType<TimelineEntities>,
      required: true,
    },
    showLimit: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      showMore: false,
    };
  },
  computed: {
    entitiesToShow(): TimelineEntities {
      if (!this.showLimit || this.showMore) {
        return this.timelineEntities;
      }
      return this.timelineEntities.slice(0, this.showLimit);
    },
  },
  methods: {
    showMoreClicked(): void {
      this.showMore = true;
      this.$nextTick().then(() => this.setVerticalLine());
    },
    setVerticalLine(): void {
      const verticalLine = this.$refs.verticalLine as HTMLDivElement;
      const wrapperEl = this.$refs.wrapper as HTMLDivElement;
      const { height } = wrapperEl.getBoundingClientRect();
      verticalLine.style.height = `${height}px`;
    },
  },
  mounted(): void {
    this.setVerticalLine();
  },
});
</script>

<style lang="scss">
.vertical-timeline {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 360px;

  @media screen and (max-width: $TINY_DISPLAY_SIZE) {
    min-width: 260px;
  }

  // TODO: Should this be used?
  @media screen and (max-width: $TINY_PHONE_RARELY_USED_SIZE) {
    min-width: 150px;
  }

  .section-body {
    display: flex;
    align-items: center;

    .wrapper {
      display: flex;
      flex-direction: row;
      align-items: center;
      height: 100%;
    }

    .vertical-line {
      height: calc(100% - 40px);
      width: 4px;
      margin-top: 32px;
      background: $primaryDark;
    }

    ul {
      margin: 0;
      padding: 0;
      flex: 1;
      z-index: 1;
      list-style-type: none; /* Remove bullets */

      // Common card styles
      li {
        display: flex;
        flex-direction: row;

        .list-item-bullet {
          position: absolute;
          width: 12px !important;
          height: 12px !important;
          border-radius: 50%;
          background-color: $primary;
          top: 24px;
          left: -8px;
        }

        .list-item-content {
          display: flex;
          flex-direction: column;
          font-size: 2.5rem;
          text-align: left;
          padding: 4px 20px;
          color: $primary;

          .list-item-item {
            display: flex;
            flex-direction: row;
            margin: 2px 4px;
            font-size: 1rem;
            color: $fontColor;

            @media screen and (max-width: $SMALL_DISPLAY_SIZE) {
              font-size: 0.8rem;
            }

            &.title {
              font-size: 1.2rem;
              font-weight: 800;
              color: $primary;
            }

            .icon {
              margin-right: 4px;
              color: $primaryDark;
              width: 20px;
            }

            .text {
              max-width: 80%;
            }
          }
        }
      }
    }
  }

  .show-more-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-items: flex-end;

    .show-more {
      display: flex;
      font-size: 1rem;
      padding: 4px;
      border-radius: 4px;
      transition: 0.3s all;

      svg {
        margin: 0 4px;
      }

      span {
        margin: 0 4px;
      }

      &:hover {
        cursor: pointer;
        background: $primary;
        color: white;
      }
    }
  }
}
</style>
