<template>
  <main>
      <Home v-if="currView === 'home'"/>
  </main>
</template>

<script>
import { bus } from '@/main';
import Home from '@/components/Views/Home.vue';

export default {
    name: 'MainContentContainer',
    components: {
        Home,
    },
    data() {
        return {
            currView: 'home',
        };
    },
    methods: {
        handleViewChanged(clickedIconName) {
            this.currView = clickedIconName;
        },
    },
    mounted() {
        bus.$on('navIconClicked', this.handleViewChanged);
    },
};
</script>

<style lang='scss'>
main {
    flex: 1;
    background-color: $secondary;
    display: flex;
    align-items: center;
}

</style>
