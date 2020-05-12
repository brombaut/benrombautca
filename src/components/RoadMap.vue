<template>
  <div class="road-map">
    <h2
      class="year-selector"
      :class="{'selected':  roadmap.year === openedYear }"
      @click="yearClicked()">
      {{ roadmap.year }}
      <div
        v-if="roadmap.year !== openedYear"
        class="expand-icon" >
        <font-awesome-icon
          :icon="['fas', 'ellipsis-h']"
          class="expand-road-map"
        />
      </div>
    </h2>
    <div ref="accordionContent" class="content">
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
            <div class="action-item-description">
              <div class='icon-container'>
                <font-awesome-icon
                  v-if="actionItem.done"
                  :icon="['fas', 'check']"
                  class="task-done"
                />
                <font-awesome-icon
                  v-else
                  :icon="['fas', 'circle']"
                  class="task-not-done"
                />
              </div>
              {{ actionItem.description }}
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component, Vue, Prop, Watch
} from "vue-property-decorator";
import { YearlyRoadmap } from "../types/yearly-roadmap";

@Component
export default class RoadMap extends Vue {
  @Prop()
  private roadmap!: YearlyRoadmap;

  @Prop()
  private openedYear!: number;

  @Watch("openedYear")
  toggleAccordionContent() {
    const content = this.$refs.accordionContent as HTMLDivElement;
    if (this.roadmap.year === this.openedYear) {
      // content.style.maxHeight = `${content.scrollHeight}px`;
      content.style.maxHeight = "none";
      content.style.opacity = "1";
    } else {
      content.style.maxHeight = "";
      content.style.opacity = "0";
    }
  }

  yearClicked() {
    this.$emit("yearClicked", this.roadmap.year);
  }

  mounted() {
    setTimeout(this.toggleAccordionContent, 1000);
  }
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

.year-selector {
  transition: color 0.3s ease-out;
  display: flex;

  .expand-icon {
    margin-left: 20px;
  }

  &:hover {
    cursor: pointer;
    color: $primary;
  }

  &.selected {
    color: $primary;
  }
}

.content {
  margin: 16px;
  transition: max-height 0.0s ease-out, opacity 0.8s ease-out;
  overflow: hidden;
  max-height: 0;
  opacity: 0;

  .task {
    margin: 8px 0;

    .description {
      color: $primary;
      margin: 0;
    }

    .action-items-list {
      list-style-type: none;
      padding-inline-start: 20px;

      li {
        font-size: 1rem;
        text-align: left;
        color: $primaryDark;
        margin: 4px 0;

        .action-item-description {
          color: white;
          display: flex;
          align-items: center;

          .icon-container {
            min-width: 24px;
            color: $primaryDark;
            align-self: flex-start;

            .task-done {
              font-size: 0.8rem;
            }

            .task-not-done {
              font-size: 0.5rem;
              padding-bottom: 2px;
            }
          }
        }
      }
    }
  }
}


</style>
