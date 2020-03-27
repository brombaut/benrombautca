<template>
  <main>
      <div class='headers-container'>
        <h1 class='main-header'>Ben Rombaut</h1>
        <h4 class='sub-header'>Software Developer</h4>
      </div>
      <MicrochipArt />
      <ConnectorElement1 />
  </main>
</template>

<script>
import MicrochipArt from '@/components/Home/MicrochipArt.vue';
import ConnectorElement1 from '@/components/ConnectorElements/ConnectorElement1.vue';

export default {
    name: 'Home',
    components: {
        MicrochipArt,
        ConnectorElement1,
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
        z-index: 1;
        padding: 60px;
        .main-header {
            color: $primary;
            font-size: 100px;
            text-align: right;
            animation: colorChange $pulseAnimationTime infinite;
        }

        .sub-header {
            color: $primaryDark;
            font-size: 40px;
            text-align: right;
            animation: colorChange $pulseAnimationTime infinite;
        }

        @keyframes colorChange {
            0% {
                color: $primaryPulse1;
            }
            25% {
                color: $primaryPulse2;
            }
            50% {
                color: $primaryPulse3;
            }
            75% {
                color: $primaryPulse4;
            }
            100% {
                color: $primaryPulse1;
            }
        }
    }
}

</style>
