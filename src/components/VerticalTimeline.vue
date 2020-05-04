<template>
  <div class="vertical-timeline">
    <div class="section-header">
      <font-awesome-icon :icon="['fas', icon]" />
      <h4 class="section-title">{{ title }}</h4>
    </div>
    <div class="section-body">
      <div class="vertical-line"></div>
      <ul v-if="type === 'education'">
        <EducationCard
          v-for="education in timelineEntities"
          :key="education.title"
          :education="education" />
      </ul>
      <ul v-else-if="type === 'work'">
        <WorkCard
          v-for="work in timelineEntities"
          :key="work.title"
          :work="work" />
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import EducationCard from "@/components/EducationCard.vue";
import WorkCard from "@/components/WorkCard.vue";
import { Education } from "../types/education";
import { Work } from "../types/work";
import { TimelineEntities } from "../types/timeline-entities";


@Component({
  components: {
    EducationCard,
    WorkCard
  }
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
}
</script>

<style lang="scss">
.vertical-timeline {
  display: flex;
  flex-direction: column;
  margin: 0 36px;

  &:hover {
    .section-header {
      color: $primary;
    }
  }

  .section-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    transition: 0.3s color;

    .section-title {
      margin: 0 8px;
      font-size: 1.2rem;
    }
  }

  .section-body {
    display: flex;
    align-items: center;
    height: fit-content;

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
    }
  }
}
</style>
