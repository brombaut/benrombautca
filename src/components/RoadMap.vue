<template>
  <div class="road-map">
    <h2>{{ roadmap.year }}</h2>
    <div class="content">
      <div
        v-for="task in roadmap.tasks"
        :key="task.description"
        class="task">
        <h4 class="description">{{ task.description }}</h4>
        <ul class="action-items-list">
          <li
            v-for="actionItem in task.actionItems"
            :key="actionItem.description"
            class="action-item">
            <div>{{ actionItem.description }}</div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { YearlyRoadmap } from "../types/yearly-roadmap";

@Component
export default class RoadMap extends Vue {
  @Prop()
  private roadmap!: YearlyRoadmap;
}
</script>

<style lang="scss" scoped>
.road-map {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}

.content,
.task {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.content {
  margin: 16px;

  .task {
    margin: 8px 0;

    .description {
      color: $primary;
      margin: 0;
    }

    .action-items-list {
      li {
        font-size: 1rem;
        text-align: left;
        color: white;
        margin: 4px 0;
      }
    }
  }
}


</style>
