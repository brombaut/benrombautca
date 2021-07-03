<template>
  <div class="tag">{{ tag }}</div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class Tag extends Vue {
  @Prop()
  tag!: string;
}
</script>

<style lang="scss">
.tag {
  font-size: 0.8em;
  font-weight: bold;
  margin: 4px 0;
  margin-right: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  color: $secondary;
  background-color: $primaryDark;
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .tag {
    font-size: 0.7em;
    margin-right: 8px;
    padding: 4px 8px;
  }
}
</style>
