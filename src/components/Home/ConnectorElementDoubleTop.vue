<template>
    <div
        class='connector-element-double'
        :class="isHovering ? 'is-hovering': ''">
        <div class='point start-point-middle'>
            <div class='highlight-point'>
                <div class='inner-point'></div>
            </div>
        </div>
        <div class='outer start-middle'>
            <div class='highlight'></div>
        </div>
        <div class='outer slant-up'>
            <div class='highlight'></div>
        </div>
        <div class='outer slant-down'>
            <div class='highlight'></div>
        </div>
        <div class='outer end-high'>
            <div class='highlight'></div>
        </div>
        <div class='outer end-low'>
            <div class='highlight'></div>
        </div>
        <div class='point end-point-high'>
            <div class='highlight-point'>
                <div class='inner-point'></div>
            </div>
        </div>
        <div class='point end-point-low'>
            <div class='highlight-point'>
                <div class='inner-point'></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ConnectorElementDouble',
    data() {
        return {
            isHovering: false,
        };
    },
    methods: {
        emitHoveringStatus(isEnter) {
            this.$emit('hoveringEvent', isEnter);
        },
        setIsHovering(newVal) {
            this.isHovering = newVal;
        },
    },
};
</script>

<style lang='scss'>
$connectorELementHeight: 16px;
$connectorELementHighlightWidth: 2px;

.connector-element-double {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;

    &.is-hovering {
        .highlight {
            animation: $backgroundHihglightAnimationQuick;
        }

        .point {
            .highlight-point {
                animation: $backgroundHihglightAnimationQuick,
            }
        }
    }

    .outer {
        height: $connectorELementHeight;
        background: $secondaryDark;
        display: flex;
        align-items: center;
        justify-content: center;
        position: absolute;
        transform-origin: 0% 50%;
    }

    .highlight {
        position: absolute;
        background: $primary;
        animation: $backgroundHihglightAnimation;
        width: calc(100% + 2px);
        height: $connectorELementHighlightWidth;
        top: calc(6px);
    }

    .point {
        position: absolute;
        height: 32px;
        width: 32px;
        border-radius: 50%;
        background: $secondaryDark;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1;

        .highlight-point {
            height: 20px;
            width: 20px;
            border-radius: 50%;
            background: $primaryDark;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
            animation: $backgroundHihglightAnimation;

            .inner-point {
                height: 14px;
                width: 14px;
                border-radius: 50%;
                background: $secondaryDark;
            }
        }
    }

    $sin45Times200: 141px;
    $cos45Times200: 141px;
    $sin25Times230: 97px;
    $cos25Times230: 208px;

    $pointTopOffset: 8px;
    $pointLeftOffset: 10px;

    $startPointMiddleTop: 150px;
    $startPointMiddleLeft: 100px;

    $outerRadius: 8px;
    $outerWidthPad: 4px;

    $startMiddleTop: $startPointMiddleTop;
    $startMiddleLeft: $startPointMiddleLeft;
    $startMiddleWidth: max(400px, 35%);
    $startMiddleRotate: 0deg;

    $slantUpTop: #{$startMiddleTop};
    $slantUpLeft: calc(#{$startPointMiddleLeft} + #{$startMiddleWidth});
    $slantUpWidth: calc(230px + #{$outerWidthPad});
    $slantUpRotate: -25deg;

    $slantDownTop: #{$startMiddleTop};
    $slantDownLeft: calc(#{$startPointMiddleLeft} + #{$startMiddleWidth});
    $slantDownWidth: calc(200px + #{$outerWidthPad});
    $slantDownRotate: 45deg;

    $endHighTop: calc(#{$slantUpTop} - #{$sin25Times230});
    $endHighLeft: calc(#{$slantUpLeft} + #{$cos25Times230});
    $endHighWidth: calc(100% - #{$endHighLeft} - 300px);
    $endHighRotate: 0deg;

    $endLowTop: calc(#{$slantDownTop} + #{$sin45Times200});
    $endLowLeft: calc(#{$slantDownLeft} + #{$cos45Times200});
    $endLowWidth: calc(100% - #{$endLowLeft} - 200px);
    $endLowRotate: 0deg;

    $endPointHighTop: $endHighTop;
    $endPointHighLeft: calc(#{$endHighLeft} + #{$endHighWidth});

    $endPointLowTop: $endLowTop;
    $endPointLowLeft: calc(#{$endLowLeft} + #{$endLowWidth});


    .start-point-middle {
        top: calc(#{$startPointMiddleTop} - #{$pointTopOffset});
        left: calc(#{$startPointMiddleLeft} - #{$pointLeftOffset});
    }
    .start-middle {
        width: calc(#{$startMiddleWidth} + #{$outerWidthPad});
        top: $startMiddleTop;
        left: $startMiddleLeft;
        transform: rotate(#{$startMiddleRotate});
        border-top-right-radius: $outerRadius;
    }
    .slant-up {
        width: $slantUpWidth;
        top: $slantUpTop;
        left: $slantUpLeft;
        transform: rotate(#{$slantUpRotate});
        border-top-left-radius: $outerRadius;
        border-bottom-right-radius: $outerRadius;
    }
    .slant-down {
        width: $slantDownWidth;
        top: $slantDownTop;
        left: $slantDownLeft;
        transform: rotate(#{$slantDownRotate});
        border-top-left-radius: $outerRadius;
        border-bottom-right-radius: $outerRadius;
    }
    .end-high {
        width: $endHighWidth;
        top: $endHighTop;
        left: $endHighLeft;
        transform: rotate(#{$endHighRotate});
        border-bottom-left-radius: $outerRadius;
    }
    .end-low {
        width: $endLowWidth;
        top: $endLowTop;
        left: $endLowLeft;
        transform: rotate(#{$endLowRotate});
        border-bottom-left-radius: $outerRadius;
    }
    .end-point-high {
        left: calc(#{$endPointHighLeft} - #{$pointLeftOffset});
        top: calc(#{$endPointHighTop} - #{$pointTopOffset});
    }
    .end-point-low {
        left: calc(#{$endPointLowLeft} - #{$pointLeftOffset});
        top: calc(#{$endPointLowTop} - #{$pointTopOffset});
    }
}
</style>
