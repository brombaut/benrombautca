<template>
  <section id="software">
    <SectionHeader title="Software" icon="code" />
    <div class="section-body">
      Software
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
export default class SoftwareSection extends Vue {

}
</script>

<style lang="scss">
#software {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
}
</style>
