<template>
  <div class="external-profile-link">
    <a
      class="link"
      :href="profile.url()"
      @click.stop.prevent="handleExternalProfileClicked()">
      <font-awesome-icon
        class="icon"
        :icon="profile.icon()"
      />
    </a>
    <div class="label">{{ profile.id() }}</div>
  </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";
import ExternalProfile from "./external-profile";

export default defineComponent({
  name: "ExternalProfileIcon",
  props: {
    profile: {
      type: Object as PropType<ExternalProfile>,
      required: true,
    },
  },
  methods: {
    handleExternalProfileClicked() {
      if (this.profile.url()) {
        const result: Window | null = window.open(this.profile.url(), "_blank");
        if (result) {
          result.focus();
        }
      }
    },
  },
});
</script>

<style lang="scss">
.external-profile-link {
  margin: 0 4px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 3em;
  font-size: 1em;

  .icon{
    margin: 8px 0px;
    color: inherit;
    transition: 0.3s;
    color: $secondary;
    z-index: 1;
    font-size: 2em;
  }

  .label {
    white-space: nowrap;
    opacity: 0;
    transition: 0.1s all ease-in;
  }

  &:hover {
    cursor: pointer;

    .icon {
      color: $secondaryDark;
    }

    .label {
      opacity: 1;
    }
  }
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  .external-profile-link {
    font-size: 0.8em;
    margin: 0 12px;
  }
}

  @media only screen and (max-width: $TINY_DISPLAY_SIZE) {
    .external-profile-link {
      font-size: 0.6em;
      margin: 0 6px;
    }
  }
</style>
