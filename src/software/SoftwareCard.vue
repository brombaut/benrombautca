<template>
  <div
    class="software-card"
    @click="cardClicked">
    <div class="dates">
      Created {{ formatDate(software.createdAt) }} • Updated {{ formatDate(software.updatedAt) }}
    </div>
    <h2 class="title">{{ software.title }}</h2>
    <div class="description"><p>{{software.description}}</p></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Tag from "@/shared/Tag.vue";
import { SoftwareArticle } from "./SoftwareArticlesProxy";

@Component({
  components: {
    Tag,
  },
})
export default class ArticleCard extends Vue {

  @Prop()
  software!: SoftwareArticle;

  formatDate(d: Date) {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  }

  cardClicked() {
    this.$emit("clicked", this.software);
  }
}
</script>

<style lang='scss'>
.software-card {
  background-color: $secondary;
  border-radius: 16px;
  margin: 12px 20px;
  padding: 24px 32px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid $secondaryDark;
  transition: 0.1s;

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
    padding: 12px 24px;

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
    padding: 8px 16px;

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
