<template>
  <a
    class="full-nav-item"
    tabindex="0"
    @click="navigate"
    @keydown.enter="navigate">
    <span>{{ text }}</span>
    <span class="underline" />
  </a>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "FullNavItem",
  props: {
    route: {
      type: String,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
  },
  methods: {
    navigate(): void {
      if (this.route !== this.$route.path) {
        this.$router.push(this.route);
        this.$emit("clicked", this.$el);
      }
    },
  },
});
</script>

<style lang="scss">
.full-nav-item {
  padding: 12px 16px 8px 16px;
  font-size: 0.9em;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-weight: bold;
  white-space: nowrap;
  font-size: 0.9em;

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

</style>
