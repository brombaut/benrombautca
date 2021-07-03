<template>
  <a
    class="full-nav-item"
    @click="navigate">
    <span>{{ text }}</span>
    <span class="underline"></span>
  </a>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class FullNavItem extends Vue {
  @Prop()
  route!: string;

  @Prop()
  text!: string;

  private navigate(): void {
    if (this.route !== this.$route.path) {
      this.$router.push(this.route);
      this.$emit("clicked", this.$el);
      // this.updateHighlight(refName);
    }
  }
}
</script>

<style lang="scss">
.full-nav-item {
  padding-top: 20px;
  padding-bottom: 12px;
  padding-left: 28px;
  padding-right: 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-weight: bold;

  .underline {
    background: white;
    height: 4px;
    width: 0;
    border-radius: 4px;
    margin-top: 2px;
    transition: 0.2s all ease-in;
  }

  &.active {
    .underline {
      width: 100%;
    }
  }

  &:hover {
    cursor: pointer;
    text-decoration: none;

    .underline {
      width: 100%;
    }
  }
}

@media only screen and (max-width: 550px) {
  .full-nav-item {
    padding: 8px 16px;
    font-size: 0.9em;
  }
}

</style>
