<template>
    <div class='connector-element-1'>
        <div class='end-point end-point-1'>
            <div class='highlight-point'>
                <div class='inner-point'></div>
            </div>
        </div>
        <div class='outer outer-1'>
            <div class='highlight'></div>
        </div>
        <div class='outer outer-2'>
            <div class='highlight'></div>
        </div>
        <div class='outer outer-3'>
            <div class='highlight'></div>
        </div>
        <div class='end-point end-point-2'>
            <div class='highlight-point'>
                <div class='inner-point'></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ConnectorElement1',
};
</script>

<style lang='scss'>
$connectorELementHeight: 16px;
$connectorELementHighlightWidth: 2px;

.connector-element-1 {
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
        // z-index: 2;
    }

    .end-point {
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

    $sin45: 0.7071;
    $cos45: 0.7071;

    $endPointTopOffset: 8px;
    $endPointLeftOffset: 10px;

    $endPoint1Top: 100px;
    $endPoint1Left: 100px;

    $outerRadius: 4px;
    $outerWidthPad: 4px;

    $outer1Top: $endPoint1Left;
    $outer1Left: $endPoint1Top;
    $outer1Width: 500px;
    $outer1Rotate: 0deg;

    $outer2Top: #{$outer1Top};
    $outer2Left: calc(#{$endPoint1Top} + #{$outer1Width});
    $outer2Width: calc(200px + #{$outerWidthPad});
    $outer2Rotate: 45deg;

    $outer3Top: 241px;
    $outer3Left: 741px;
    $outer3Width: 500px;
    $outer3Rotate: 0deg;

    $endPoint2Top: $outer3Top;
    $endPoint2Left: calc(#{$outer3Left} + #{$outer1Width});


    .end-point-1 {
        top: calc(#{$endPoint1Top} - #{$endPointTopOffset});
        left: calc(#{$endPoint1Left} - #{$endPointLeftOffset});
    }
    .outer-1 {
        width: calc(#{$outer1Width} + #{$outerWidthPad});
        top: $outer1Top;
        left: $outer1Left;
        transform: rotate(#{$outer1Rotate});
        border-top-right-radius: $outerRadius;
    }
    .outer-2 {
        width: $outer2Width;
        top: $outer2Top;
        left: $outer2Left;
        transform: rotate(#{$outer2Rotate});
        border-top-left-radius: $outerRadius;
        border-bottom-right-radius: $outerRadius;
    }
    .outer-3 {
        width: $outer3Width;
        top: $outer3Top;
        left: $outer3Left;
        transform: rotate(#{$outer3Rotate});
        border-bottom-left-radius: $outerRadius;
    }
    .end-point-2 {
        left: calc(#{$endPoint2Left} - #{$endPointLeftOffset});
        top: calc(#{$endPoint2Top} - #{$endPointTopOffset});
    }

}
</style>
