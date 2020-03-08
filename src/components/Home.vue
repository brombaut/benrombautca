<template>
  <main>
      <div class='headers-container'>
        <h1 class='main-header'>Ben Rombaut</h1>
        <h4 class='sub-header'>Software Developer</h4>
      </div>
  </main>
</template>

<script>
export default {
    name: 'Home',
};
</script>

<style lang='scss'>
main {
    flex: 1;
    background-color: #1c1d25;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    position: relative;
    padding: 100px;

    .headers-container {
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
