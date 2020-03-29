<template>
    <div
        id='microchip'
        v-if="showMicrochip"
        :class="isHovering ? 'is-hovering': ''"
        @mouseenter="emitHoveringStatus(true)"
        @mouseleave="emitHoveringStatus(false)">
        <!-- Top Connectors -->
        <div class='horizontal-connectors-container'>
            <div
                v-for="i in numberOfConnectors"
                :key="i"
                class='long-connector'>
            </div>
        </div>
        <div class='middle-chip-elements-container'>
            <!-- Left Connectors -->
            <div class='vertical-connectors-container'>
                <div
                    v-for="i in numberOfConnectors"
                    :key="i"
                    class='wide-connector'>
                </div>
            </div>
            <!-- Chip Outline -->
            <div class='outer-border'>
                <div class='highlight-border'>
                    <div class='inner-border'>
                        <div class='base-square'>

                            <div
                                v-for="i in numberOfConnectors"
                                :key="i"
                                class='end-point'
                                :class="'end-point-' + i">
                                <div class='highlight-point'>
                                    <div class='inner-point'></div>
                                </div>
                            </div>

                            <div class='end-point-connection-1'></div>
                            <div class='end-point-connection-2'></div>
                            <div class='end-point-connection-3'></div>
                            <div class='end-point-connection-4'></div>
                            <div class='end-point-connection-5'></div>
                            <div class='end-point-connection-6'></div>
                            <div class='end-point-connection-7'></div>
                            <div class='end-point-connection-8'></div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Right Connectors -->
            <div class='vertical-connectors-container'>
                <div
                    v-for="i in numberOfConnectors"
                    :key="i"
                    class='wide-connector'>
                </div>
            </div>
        </div>
        <!-- Bottom Connectors -->
        <div class='horizontal-connectors-container'>
            <div
                v-for="i in numberOfConnectors"
                :key="i"
                class='long-connector'>
            </div>
        </div>

    </div>
</template>

<script>
import { bus } from '@/main';

export default {
    name: 'MicrochipArt',
    data() {
        return {
            numberOfConnectors: 8,
            isHovering: false,
            showMicrochip: true,
        };
    },
    methods: {
        emitHoveringStatus(isEnter) {
            this.$emit('hoveringEvent', isEnter);
        },
        setIsHovering(newVal) {
            this.isHovering = newVal;
        },
        setMicrochipIsVisible(isVisible) {
            this.isVisible = isVisible;
        },
        handleWindowResize(e) {
            const windowWidth = window.innerWidth;
            if (this.showMicrochip && windowWidth < 1350) {
                this.showMicrochip = false;
            } else if (!this.showMicrochip && windowWidth >= 1350) {
                this.showMicrochip = true;
            }
        },
    },
    mounted() {
        window.addEventListener('resize', this.handleWindowResize);
        this.handleWindowResize();
    },
};
</script>

<style lang='scss'>
$connectorLongPixels: 40px;
$connectorShortPixels: 8px;


#microchip {
    position: absolute;
    top: 25%;
    left: 10%;
    z-index: 1;

    .horizontal-connectors-container {
        margin: 0 40px;
        padding: 8px 16px;
        display: flex;
        justify-content: space-around;
        align-items: center;

        .long-connector {
            height: $connectorLongPixels;
            width: $connectorShortPixels;
            background: $secondaryDark;
            border-radius: 4px;;
        }
    }

    .middle-chip-elements-container {
        display: flex;
    }

    .vertical-connectors-container {
        padding: 16px 8px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;

        .wide-connector {
            height: $connectorShortPixels;
            width: $connectorLongPixels;
            background: $secondaryDark;
            border-radius: 4px;;
        }
    }

    .outer-border {
        height: 300px;
        width: 300px;
        border: 16px solid $secondaryDark;
        border-radius: 16px;
        box-sizing: border-box;

        .highlight-border {
            box-sizing: border-box;
            height: 100%;
            width: 100%;
            border: 4px solid $primaryDark;
            border-radius: 4px;
            transition: border 0.3s;
            animation: $borderHighlightAnimation;

            .inner-border {
                box-sizing: border-box;
                height: 100%;
                width: 100%;
                border: 16px solid $secondaryDark;
                position: relative;

                .base-square {
                    position: absolute;
                    box-sizing: content-box;
                    border-radius: 16px;
                    height: calc(100% + 0px);
                    width: calc(100% + 0px);
                    top: -0px;
                    left: -0px;
                    background: $secondary;
                }
            }
        }
    }

    .end-point {
        position: absolute;
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: $secondaryDark;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1;

        .highlight-point {
            height: 16px;
            width: 16px;
            border-radius: 50%;
            background: $primaryDark;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
            animation: $backgroundHihglightAnimation;

            .inner-point {
                height: 10px;
                width: 10px;
                border-radius: 50%;
                background: $secondaryDark;
            }
        }
    }

    $endPoint1Top: 10%;
    $endPoint1Left: 20%;
    .end-point-1 {
        top: $endPoint1Top;
        left: $endPoint1Left;
    }
    .end-point-connection-1 {
        position: absolute;
        width: calc(#{$endPoint1Left} + 4px);
        height: 10px;
        top: calc(#{$endPoint1Top} + 6px);
        left: 0;
        background: $secondaryDark;
    }

    $endPoint2Top: 10%;
    $endPoint2Left: 60%;
    .end-point-2 {
        top: $endPoint2Top;
        left: $endPoint2Left;
    }
    .end-point-connection-2 {
        position: absolute;
        height: calc(#{$endPoint2Top} + 4px);
        width: 10px;
        top: 0;
        left: calc(#{$endPoint2Left} + 7px);
        background: $secondaryDark;
    }

    $endPoint3Top: 40%;
    $endPoint3Left: 20%;
    .end-point-3 {
        top: $endPoint3Top;
        left: $endPoint3Left;
    }
    .end-point-connection-3 {
        position: absolute;
        width: calc(#{$endPoint3Left} + 4px);
        height: 10px;
        top: calc(#{$endPoint3Top} + 6px);
        left: 0;
        background: $secondaryDark;
    }

    $endPoint4Top: 33%;
    $endPoint4Left: 60%;
    .end-point-4 {
        top: $endPoint4Top;
        left: $endPoint4Left;
    }
    .end-point-connection-4 {
        position: absolute;
        width: calc(100% - #{$endPoint4Left} + 4px);
        height: 10px;
        top: calc(#{$endPoint4Top} + 6px);
        left: calc(#{$endPoint4Left} + 7px);
        background: $secondaryDark;
    }

    $endPoint5Top: 50%;
    $endPoint5Left: 70%;
    .end-point-5 {
        top: $endPoint5Top;
        left: $endPoint5Left;
    }
    .end-point-connection-5 {
        position: absolute;
        width: calc(100% - #{$endPoint5Left} + 4px);
        height: 10px;
        top: calc(#{$endPoint5Top} + 6px);
        left: calc(#{$endPoint5Left} + 7px);
        background: $secondaryDark;
    }

    $endPoint6Top: 70%;
    $endPoint6Left: 20%;
    .end-point-6 {
        top: $endPoint6Top;
        left: $endPoint6Left;
    }
    .end-point-connection-6 {
        position: absolute;
        height: calc(100% - #{$endPoint6Top} + 4px);
        width: 10px;
        top: calc(#{$endPoint6Top} + 4px);
        left: calc(#{$endPoint6Left} + 7px);
        background: $secondaryDark;
    }

    $endPoint7Top: 80%;
    $endPoint7Left: 35%;
    .end-point-7 {
        top: $endPoint7Top;
        left: $endPoint7Left;
    }
    .end-point-connection-7 {
        position: absolute;
        height: calc(100% - #{$endPoint7Top} + 4px);
        width: 10px;
        top: calc(#{$endPoint7Top} + 4px);
        left: calc(#{$endPoint7Left} + 7px);
        background: $secondaryDark;
    }

    $endPoint8Top: 67%;
    $endPoint8Left: 60%;
    .end-point-8 {
        top: $endPoint8Top;
        left: $endPoint8Left;
    }
    .end-point-connection-8 {
        position: absolute;
        height: calc(100% - #{$endPoint8Top} + 4px);
        width: 10px;
        top: calc(#{$endPoint8Top} + 4px);
        left: calc(#{$endPoint8Left} + 7px);
        background: $secondaryDark;
    }

    &.is-hovering {
        .highlight-border {
            animation: $borderHighlightAnimationQuick;
        }

        .highlight-point {
            animation: $backgroundHihglightAnimationQuick,
        }
    }
}

</style>
