<template>
  <div class='icon-container' @click="handleIconClick">
        <font-awesome-icon :icon="[iconStyle, iconName]" />
    </div>
</template>

<script>
import { bus } from '@/main';

export default {
    name: 'NavBarIcon',
    props: {
        iconStyle: String,
        iconName: String,
    },
    methods: {
        handleIconClick() {
            bus.$emit('navIconClicked', this.$el.getBoundingClientRect());
        },
    },
};
</script>

<style lang='scss'>
.icon-container {
    padding: 12px 0;
    margin: 8px 0;
    font-size: 32px;
    transition: 0.3s;
    z-index: 1;
    width: 60px;

    &:hover {
        color: lighten(#2c3e50, 20%);
        cursor: pointer;
    }
}

</style>
