<template>
    <div class='connector-element-single-upward'>
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
        <div class='outer end-high'>
            <div class='highlight'></div>
        </div>
        <div class='point end-point-high'>
            <div class='highlight-point'>
                <div class='inner-point'></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ConnectorElementSingleUpward',
};
</script>

<style lang='scss' scoped>
$connectorELementHeight: 16px;
$connectorELementHighlightWidth: 2px;

.connector-element-single-upward {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 0;

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
        animation: $backgroundHihglightDimmedAnimation;
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
            animation: $backgroundHihglightDimmedAnimation;

            .inner-point {
                height: 14px;
                width: 14px;
                border-radius: 50%;
                background: $secondaryDark;
            }
        }
    }

    @keyframes backgroundColorChange {
        0% {
            background: $primaryPulse1;
        }
        25% {
            background: $primaryPulse2;
        }
        50% {
            background: $primaryPulse3;
        }
        75% {
            background: $primaryPulse4;
        }
        100% {
            background: $primaryPulse1;
        }
    }

    $sin45Times200: 141px;
    $cos45Times200: 141px;

    $pointTopOffset: 8px;
    $pointLeftOffset: 10px;

    $startPointMiddleTop: 270px;
    $startPointMiddleLeft: 180px;

    $outerRadius: 4px;
    $outerWidthPad: 4px;

    $startMiddleTop: $startPointMiddleTop;
    $startMiddleLeft: $startPointMiddleLeft;
    $startMiddleWidth: max(400px, 35%);
    $startMiddleRotate: 0deg;

    $slantUpTop: #{$startMiddleTop};
    $slantUpLeft: calc(#{$startPointMiddleLeft} + #{$startMiddleWidth});
    $slantUpWidth: calc(200px + #{$outerWidthPad});
    $slantUpRotate: -45deg;

    $endHighTop: calc(#{$slantUpTop} - #{$sin45Times200});
    $endHighLeft: calc(#{$slantUpLeft} + #{$cos45Times200});
    $endHighWidth: calc(100% - #{$endHighLeft} - 100px);
    $endHighRotate: 0deg;

    $endPointHighTop: $endHighTop;
    $endPointHighLeft: calc(#{$endHighLeft} + #{$endHighWidth});


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
    .end-high {
        width: $endHighWidth;
        top: $endHighTop;
        left: $endHighLeft;
        transform: rotate(#{$endHighRotate});
        border-bottom-left-radius: $outerRadius;
    }
    .end-point-high {
        left: calc(#{$endPointHighLeft} - #{$pointLeftOffset});
        top: calc(#{$endPointHighTop} - #{$pointTopOffset});
    }

}
</style>
