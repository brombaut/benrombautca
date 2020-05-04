<template>
  <div class="vertical-timeline">
    <div class="section-header">
      <font-awesome-icon :icon="['fas', 'user']" />
      <h4 class="section-title">EDUCATION</h4>
    </div>
    <div class="section-body">
      <div class="vertical-line"></div>
      <ul>
        <EducationCard
          v-for="education in educationEntities"
          :key="education.title"
          :education="education" />
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import educationEntities from "@/data/educationEntities";
import EducationCard from "@/components/EducationCard.vue";
import { Education } from "../types/education";

@Component({
  components: {
    EducationCard
  }
})
export default class VerticalTimeline extends Vue {
  private educationEntities: Education[] = educationEntities;
}
</script>

<style lang="scss">
.vertical-timeline {
  display: flex;
  flex-direction: column;

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
    flex: 1;
    align-items: center;

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
