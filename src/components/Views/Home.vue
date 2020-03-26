<template>
  <main>
      <div class='headers-container'>
        <h1 class='main-header'>Ben Rombaut</h1>
        <h4 class='sub-header'>Software Developer</h4>
      </div>
      <MicrochipArt />
  </main>
</template>

<script>
import MicrochipArt from '@/components/Home/MicrochipArt.vue';

export default {
    name: 'Home',
    components: {
        MicrochipArt,
    },
};
</script>

<style lang='scss'>
main {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 100px;
    position: relative;

    .headers-container {
        z-index: 1;
        .main-header {
            color: white;
            font-size: 80px;
            text-align: right;
        }

        .sub-header {
            color: white;
            font-size: 40px;
            text-align: right;
        }
    }
}

</style>
