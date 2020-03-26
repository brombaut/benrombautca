<template>
  <div
    class='icon-container'
    :class='{"selected": selected}'
    @click="handleIconClick"
    @mouseover="hovering = true"
    @mouseleave="hovering = false" >
        <font-awesome-icon
            v-if="!hovering"
            :icon="[icon.iconStyle, icon.iconName]" />
        <div v-else class='hover-text'>{{ icon.hoverText }}</div>
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
            hovering: false,
        };
    },
    methods: {
        handleIconClick() {
            this.icon.iconClickCallback(this.$el.getBoundingClientRect(), this.icon.name);
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
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    user-select: none;

    &.selected {
        color: darken(#3381db, 15%);
    }

    &:hover {
        color: #3381db;
        cursor: pointer;
    }

    svg {
        animation: roteateOutZ;
        animation-duration: 0.3s;
    }

    .hover-text {
        font-size: 12px;
        animation: roteateInZ;
        animation-duration: 0.3s;
        color: #3381db;
    }

    @keyframes roteateInZ {
        from {
            transform: rotateZ(90deg);
        }
        to {
            transform: rotateZ(0deg);;
        }
    }

    @keyframes roteateOutZ {
        from {
            transform: rotateZ(-90deg);
        }
        to {
            transform: rotateZ(0deg);;
        }
    }
}

</style>
