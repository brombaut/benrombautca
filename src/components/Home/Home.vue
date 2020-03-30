<template>
    <main>
        <div class='headers-container'>
            <h1
                class='main-header'
                :class="isHovering ? 'is-hovering': ''"
                @mouseenter="updateHoveringStatus(true)"
                @mouseleave="updateHoveringStatus(false)">
                Ben Rombaut
            </h1>
            <h4
                class='sub-header'
                :class="isHovering ? 'is-hovering': ''"
                @mouseenter="updateHoveringStatus(true)"
                @mouseleave="updateHoveringStatus(false)">
                Software Developer
            </h4>
        </div>
        <MicrochipArt @hoveringEvent='updateHoveringStatus' />
        <ConnectorElementDoubleTop @hoveringEvent='updateHoveringStatus' />
        <ConnectorElementDoubleBottom @hoveringEvent='updateHoveringStatus' />
  </main>
</template>

<script>
import MicrochipArt from '@/components/Home/MicrochipArt.vue';
import ConnectorElementDoubleTop from '@/components/Home/ConnectorElementDoubleTop.vue';
import ConnectorElementDoubleBottom from '@/components/Home/ConnectorElementDoubleBottom.vue';

export default {
    name: 'Home',
    components: {
        MicrochipArt,
        ConnectorElementDoubleTop,
        ConnectorElementDoubleBottom,
    },
    data() {
        return {
            isHovering: false,
        };
    },
    methods: {
        updateHoveringStatus(isHovering) {
            this.isHovering = isHovering;
            this.$children.forEach(child => {
                if (child.setIsHovering) {
                    child.setIsHovering(isHovering);
                }
            });
        },
    },
};
</script>

<style lang='scss'>
main {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    position: relative;
    height: 100%;
    width: 100%;

    .headers-container {
        padding: 60px;
        z-index: 10;
        font-weight: 900;

        .main-header {
            color: $primary;
            font-size: 120px;
            text-align: right;
            animation: $colorHighlightAnimation;
            margin: 20px 0;
            font-weight: 600;
            -webkit-text-stroke: 1px black;

            &.is-hovering {
                animation: $colorHighlightAnimationQuick;
            }
        }

        .sub-header {
            color: $primaryDark;
            font-size: 60px;
            text-align: right;
            animation: $colorHighlightAnimation;
            margin: 0;
            font-weight: 500;
            -webkit-text-stroke: 1px black;

            &.is-hovering {
                animation: $colorHighlightAnimationQuick;
            }
        }
    }
}

</style>
