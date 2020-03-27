<template>
    <div class='connector-element-single-downward'>
        <div class='point start-point-middle'>
            <div class='highlight-point'>
                <div class='inner-point'></div>
            </div>
        </div>
        <div class='outer start-middle'>
            <div class='highlight'></div>
        </div>
        <div class='outer slant-down'>
            <div class='highlight'></div>
        </div>
        <div class='outer end-low'>
            <div class='highlight'></div>
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
    name: 'ConnectorElementSingleDownward',
};
</script>

<style lang='scss'>
$connectorELementHeight: 16px;
$connectorELementHighlightWidth: 2px;

.connector-element-single-downward {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;

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
        animation: backgroundColorChange $pulseAnimationTime infinite;
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
            animation: backgroundColorChange $pulseAnimationTime infinite;

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

    $startPointMiddleTop: 150px;
    $startPointMiddleLeft: 100px;

    $outerRadius: 4px;
    $outerWidthPad: 4px;

    $startMiddleTop: $startPointMiddleTop;
    $startMiddleLeft: $startPointMiddleLeft;
    $startMiddleWidth: max(350px, 35%);
    $startMiddleRotate: 0deg;

    $slantDownTop: #{$startMiddleTop};
    $slantDownLeft: calc(#{$startPointMiddleLeft} + #{$startMiddleWidth});
    $slantDownWidth: calc(200px + #{$outerWidthPad});
    $slantDownRotate: 45deg;

    $endLowTop: calc(#{$slantDownTop} + #{$sin45Times200});
    $endLowLeft: calc(#{$slantDownLeft} + #{$cos45Times200});
    $endLowWidth: calc(100% - #{$endLowLeft} - 200px);
    $endLowRotate: 0deg;

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
    .slant-down {
        width: $slantDownWidth;
        top: $slantDownTop;
        left: $slantDownLeft;
        transform: rotate(#{$slantDownRotate});
        border-top-left-radius: $outerRadius;
        border-bottom-right-radius: $outerRadius;
    }
    .end-low {
        width: $endLowWidth;
        top: $endLowTop;
        left: $endLowLeft;
        transform: rotate(#{$endLowRotate});
        border-bottom-left-radius: $outerRadius;
    }
    .end-point-low {
        left: calc(#{$endPointLowLeft} - #{$pointLeftOffset});
        top: calc(#{$endPointLowTop} - #{$pointTopOffset});
    }

}
</style>
