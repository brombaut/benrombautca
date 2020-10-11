<template>
  <div class="vertical-timeline">
    <SectionHeader :title="title" :icon="icon" />
    <div class="section-body">
      <div class="wrapper">
        <div class="vertical-line"></div>
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
      <div class="show-more" @click="showMoreClicked()">
        <font-awesome-icon :icon="['fas', 'caret-down']" />
        <span>SHOW MORE</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component, Vue, Prop, Watch,
} from "vue-property-decorator";
import EducationCard from "./EducationCard.vue";
import WorkCard from "./WorkCard.vue";
import { Education } from "./education";
import { Work } from "./work";
import { TimelineEntities } from "./timeline-entities";
import SectionHeader from "../shared/SectionHeader.vue";

@Component({
  components: {
    EducationCard,
    WorkCard,
    SectionHeader,
  },
})
export default class VerticalTimeline extends Vue {
  @Prop()
  private type!: string;

  @Prop()
  private title!: string;

  @Prop()
  private icon!: string;

  @Prop()
  private timelineEntities!: TimelineEntities;

  @Prop({ default: 0 })
  private showLimit!: number;

  private showMore = false;

  get entitiesToShow(): TimelineEntities {
    if (!this.showLimit || this.showMore) {
      return this.timelineEntities;
    }
    return this.timelineEntities.slice(0, this.showLimit);
  }

  showMoreClicked() {
    this.showMore = true;
    this.$nextTick().then(() => this.setVerticalLine());
  }

  setVerticalLine() {
    const verticalLine = this.$el.querySelector(
      ".vertical-line",
    ) as HTMLDivElement;
    const wrapperEl = this.$el.querySelector(".wrapper") as HTMLDivElement;
    const { height } = wrapperEl.getBoundingClientRect();
    verticalLine.style.height = `${height}px`;
  }

  mounted() {
    this.setVerticalLine();
  }
}
</script>

<style lang="scss">
.vertical-timeline {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 340px;

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
      transform: translateX(18px);
      filter: brightness(75%);
    }

    ul {
      margin: 0;
      flex: 1;
      z-index: 1;

      // Common card styles
      li {
        font-size: 2.5rem;
        text-align: left;
        padding: 4px 20px;

        div {
          margin: 4px;
          font-size: 1rem;
          transform: translateY(8px);
        }

        .title {
          font-size: 1.2rem;
          font-weight: 800;
          color: $primary;
        }

        .icon {
          margin-right: 4px;
          color: $primaryDark;
          width: 20px;
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
