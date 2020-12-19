<template>
  <a class="external-profile-link" :href="profile.url()">
    <font-awesome-icon
      class="icon"
      @click.stop.prevent="handleExternalProfileClicked()"
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
  margin: 0 20px;
  font-size: 2rem;

  .icon{
    color: inherit;
    transition: 0.3s;
    color: $secondary;
  }

  &:hover {
    cursor: pointer;

    .icon {
      color: $secondaryDarkest;
    }
  }
}
</style>
