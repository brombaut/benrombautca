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
import { Component, Vue } from "vue-property-decorator";

@Component
export default class BackButton extends Vue {
  get isVisible(): boolean {
    const currRouteName: string = this.$route.name || "";
    if (currRouteName === "selectedArticle") return true;
    if (currRouteName === "selectedSoftware") return true;
    return false;
  }

  private goBack() {
    this.$router.go(-1);
  }
}
</script>

<style lang="scss">
.back-button-wrapper {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-weight: bold;
  box-sizing: border-box;
  padding-top: 20px;
  padding-bottom: 12px;
  padding-left: 12px;
  padding-right: 12px;
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

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .back-button-wrapper {
    display: none;
  }
}

</style>
