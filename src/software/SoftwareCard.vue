<template>
  <div
    class="software-card"
    @click="cardClicked">
    <header>
      <h2 class="title">{{ software.title }}</h2>
    </header>
    <div class="body">
      <div class="dates">
        Created {{ formatDate(software.createdAt) }} • Updated {{ formatDate(software.updatedAt) }}
      </div>
      <div class="description"><p>{{software.description}}</p></div>
    </div>
    <footer>
      <ViewOnAndTechUsed :software="software" />
    </footer>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import ViewOnAndTechUsed from "./ViewOnAndTechUsed.vue";
import { SoftwareArticle } from "./SoftwareArticlesProxy";

export default Vue.extend({
  name: "SoftwareCard",
  components: {
    ViewOnAndTechUsed,
  },
  props: {
    software: {
      type: Object as PropType<SoftwareArticle>,
      required: true,
    },
  },
  methods: {
    formatDate(d: Date): string {
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
    },
    cardClicked(): void {
      this.$emit("clicked", this.software);
    },
  },
});
</script>

<style lang='scss'>
$borderRadius: 16px;
$horizontalPadding: 24px;
$verticalPadding: 8px;

.software-card {
  background-color: lighten($secondary, 2%);
  border-radius: $borderRadius;
  margin: 12px 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid $secondaryDark;
  transition: 0.1s;

  header {
    width: calc(100% - 2*$horizontalPadding);
    padding: 2*$verticalPadding $horizontalPadding $verticalPadding $horizontalPadding;
    background-color: $secondaryDark;
    border-top-left-radius: $borderRadius;
    border-top-right-radius: $borderRadius;
  }
  .body {
    width: calc(100% - 2*$horizontalPadding);
    padding: $verticalPadding $horizontalPadding $verticalPadding $horizontalPadding;
    background-color: $secondaryLight;
  }
  footer {
    width: calc(100% - 2*$horizontalPadding);
    padding: $verticalPadding $horizontalPadding 2*$verticalPadding $horizontalPadding;
    background-color: $secondary;
    border-bottom-left-radius: $borderRadius;
    border-bottom-right-radius: $borderRadius;
  }

  &:hover {
    cursor: pointer;
    box-shadow: 1px 1px 5px $pFontColor;
  }

  .dates {
    margin: 8px 0;
    font-size: 0.9em;
  }

  .title {
    color: $primary;
  }

  .description {
    font-size: 1em;
  }
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .software-card {
    margin: 12px 20px;

    .title {
      font-size: 1.5em;
    }
    .description {
      font-size: 0.9em;
    }
  }
}

@media only screen and (max-width: $TINY_DISPLAY_SIZE) {
  .software-card {
    margin: 8px 8px;

    .dates {
      margin: 8px 0;
      font-size: 0.7em;
    }
    .title {
      font-size: 1.2em;
    }
    .description {
      font-size: 0.8em;
    }
  }
}
</style>
