<template>
  <div
    class="software-card"
    role="button"
    tabindex="0"
    @click="cardClicked"
    @keydown.enter="cardClicked">
    <header>
      <h2 class="title">{{ software.title }}</h2>
      <div class="spacer" />
      <div class="external-profiles">
        <ExternalRepoIcon
          v-for="repo in software.externalRepos"
          :key="repo._id"
          :externalRepo="repo"
          :verbose="false" />
      </div>
    </header>
    <div class="body">
      <div class="dates">
        Created {{ formatDate(software.createdAt) }} • Updated {{ formatDate(software.updatedAt) }}
      </div>
      <div class="description"><p>{{software.description}}</p></div>
    </div>
    <footer>
      <TechUsedIcon
        v-for="tech in software.techUsed"
        :key="tech._id"
        :tech=tech />
    </footer>
  </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import ExternalRepoIcon from "./ExternalRepoIcon.vue";
import TechUsedIcon from "./TechUsedIcon.vue";
import { SoftwareArticle } from "./SoftwareArticlesProxy";

export default defineComponent({
  name: "SoftwareCard",
  components: {
    ExternalRepoIcon,
    TechUsedIcon,
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
$borderRadius: 4px;
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
    width: calc(100% - 24px - 24px);
    padding: 2*$verticalPadding $horizontalPadding $verticalPadding $horizontalPadding;
    background-color: $secondaryDark;
    border-top-left-radius: $borderRadius;
    border-top-right-radius: $borderRadius;

    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;

    .external-profiles {
      display: flex;
      flex-direction: row;
    }
  }
  .body {
    width: calc(100% - 24px - 24px);
    padding: $verticalPadding $horizontalPadding $verticalPadding $horizontalPadding;
    background-color: $secondaryLight;

    p {
      margin-bottom: 0;
    }
  }
  footer {
    width: calc(100% - 24px - 24px);
    padding: $verticalPadding $horizontalPadding 2*$verticalPadding $horizontalPadding;
    background-color: $secondaryLight;
    border-bottom-left-radius: $borderRadius;
    border-bottom-right-radius: $borderRadius;
    display: flex;
    flex-direction: row;
    align-items: center;
    flex-wrap: wrap;

    .footer-title {
      margin-right: 4px
    }
  }

  &:hover {
    $darkenPercent: 4%;
    cursor: pointer;

    header {
      background-color: darken($secondaryDark, $darkenPercent);
    }
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

    .external-profiles {
      display: none !important;
    }
  }
}
</style>
