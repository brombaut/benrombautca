<template>
    <div class='connector-element-double'>
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
};
</script>

<style lang='scss' scoped>
$connectorELementHeight: 16px;
$connectorELementHighlightWidth: 2px;

@media screen and (max-width: 1100px) {
    .connector-element-double {
        display: none;
    }
}

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
            transition: background-color 0.3s;
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
    $sin20Times250: 86px;
    $cos20Times250: 235px;

    $pointTopOffset: 8px;
    $pointLeftOffset: 10px;

    $startPointMiddleTop: calc(100% - 170px);
    $startPointMiddleLeft: 180px;

    $outerRadius: 4px;
    $outerWidthPad: 4px;

    $startMiddleTop: $startPointMiddleTop;
    $startMiddleLeft: $startPointMiddleLeft;
    $startMiddleWidth: 25%;
    $startMiddleRotate: 0deg;

    $slantUpTop: #{$startMiddleTop};
    $slantUpLeft: calc(#{$startPointMiddleLeft} + #{$startMiddleWidth});
    $slantUpWidth: calc(200px + #{$outerWidthPad});
    $slantUpRotate: -45deg;

    $slantDownTop: #{$startMiddleTop};
    $slantDownLeft: calc(#{$startPointMiddleLeft} + #{$startMiddleWidth});
    $slantDownWidth: calc(250px + #{$outerWidthPad});
    $slantDownRotate: 20deg;

    $endHighTop: calc(#{$slantUpTop} - #{$sin45Times200});
    $endHighLeft: calc(#{$slantUpLeft} + #{$cos45Times200});
    $endHighWidth: calc(100% - #{$endHighLeft} - 100px);
    $endHighRotate: 0deg;

    $endLowTop: calc(#{$slantDownTop} + #{$sin20Times250});
    $endLowLeft: calc(#{$slantDownLeft} + #{$cos20Times250});
    $endLowWidth: calc(100% - #{$endLowLeft} - 250px);
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
