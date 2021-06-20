<template>
  <section id="articles">
    <SectionHeader title="Articles" icon="pen-square" />
    <div class="section-body">
      Articles
    </div>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import uiUtils from "@/utils/ui-utils";
import SectionHeader from "../shared/SectionHeader.vue";

@Component({
  components: {
    SectionHeader,
  },
})
export default class ArticlesSection extends Vue {

}
</script>

<style lang="scss">
#articles {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
}
</style>
