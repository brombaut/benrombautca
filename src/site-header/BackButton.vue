<template>
<div class="back-button-wrapper" v-if="isVisible" @click="goBack">
  <a class='back-button'>
    <font-awesome-icon class='icon' :icon="['fas', 'chevron-left']"/>
    <span>Back</span>
  </a>
  <span class="underline"></span>
</div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  computed: {
    isVisible(): boolean {
      const currRouteName: string = this.$route.name || "";
      if (currRouteName === "selectedArticle") return true;
      if (currRouteName === "selectedSoftware") return true;
      return false;
    },
  },
  methods: {
    goBack(): void {
      this.$router.go(-1);
    },
  },
});
</script>

<style lang="scss">
.back-button-wrapper {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-weight: bold;
  box-sizing: border-box;
  padding: 12px 12px 12px 12px;
  font-size: 0.9em;
  left: 0;

  .back-button {
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    align-items: flex-end;
    height: 100%;
    font-weight: bold;

    .icon {
      margin-right: 4px;
      align-self: center;
    }
  }

  .underline {
    background: white;
    height: 4px;
    width: 0;
    border-radius: 4px;
    margin-top: 2px;
    transition: 0.2s all ease-in;
  }

  &:hover {
    cursor: pointer;

    .back-button {
      text-decoration: none;
    }

    .underline {
      width: 100%;
    }
  }
}

@media only screen and (max-width: $MEDIUM_DISPLAY_SIZE) {
  .back-button-wrapper {
    font-size: 0.9em;
    padding-top: 12px;
  }
}

</style>
