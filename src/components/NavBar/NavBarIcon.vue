<template>
  <div
    class='icon-container'
    :class='{"selected": selected}'
    @click="handleIconClick">
        <font-awesome-icon :icon="[icon.iconStyle, icon.iconName]" />
    </div>
</template>

<script>
import { bus } from '@/main';

export default {
    name: 'NavBarIcon',
    props: {
        icon: Object,
    },
    data() {
        return {
            selected: false,
        };
    },
    methods: {
        handleIconClick() {
            this.icon.iconClickCallback(this.$el.getBoundingClientRect(), this.icon.name);
            // bus.$emit('navIconClicked', this.$el.getBoundingClientRect());
        },
        setSelectedIfNecessary(clickedIconName) {
            this.selected = clickedIconName === this.icon.name;
        },
    },
    mounted() {
        bus.$on('navIconClicked', this.setSelectedIfNecessary);
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

    &.selected {
        color: darken(#3381db, 15%);
    }

    &:hover {
        color: #3381db;
        cursor: pointer;
    }
}

</style>
