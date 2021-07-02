<template>
  <a
    class="external-profile-link"
    :href="profile.url()"
    @click.stop.prevent="handleExternalProfileClicked()">
    <div class="hover-background"></div>
    <font-awesome-icon
      class="icon"
      :icon="profile.icon()"
    />
  </a>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import ExternalProfile from "./external-profile";

@Component
export default class ExternalProfileIcon extends Vue {

  @Prop()
  profile!: ExternalProfile;

  private handleExternalProfileClicked() {
    if (this.profile.url()) {
      const result: Window | null = window.open(this.profile.url(), "_blank");
      if (result) {
        result.focus();
      }
    }
  }
}
</script>

<style lang="scss">
.external-profile-link {
  margin: 0 16px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 3em;
  width: 3em;
  font-size: 1em;

  .hover-background {
    background-color: $primaryDarkest;
    border-radius: 50%;
    position: absolute;
    height: 0;
    width: 0;
    transition: 0.3s;
  }

  .icon{
    color: inherit;
    transition: 0.3s;
    color: $secondary;
    z-index: 1;
    font-size: 2em;
  }

  &:hover {
    cursor: pointer;

    .icon {
      color: $secondaryDark;
    }

    .hover-background {
      height: 100%;
      width: 100%;
    }
  }
}

  @media only screen and (max-width: 640px) {
    .external-profile-link {
      font-size: 0.8em;
      margin: 0 12px;
    }
  }
</style>
