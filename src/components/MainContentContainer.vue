<template>
  <main>
      <Home v-if="currView === 'home'"/>
      <AboutMe v-else-if="currView === 'aboutMe'"/>
      <Portfolio v-else-if="currView === 'portfolio'"/>
      <RecentActivity v-else-if="currView === 'recentActivity'"/>
  </main>
</template>

<script>
import { bus } from '@/main';
import Home from '@/components/Home/Home.vue';
import AboutMe from '@/components/AboutMe/AboutMe.vue';
import Portfolio from '@/components/Portfolio/Portfolio.vue';
import RecentActivity from '@/components/RecentActivity/RecentActivity.vue';

export default {
    name: 'MainContentContainer',
    components: {
        Home,
        AboutMe,
        Portfolio,
        RecentActivity,
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

h1 {
    color: $primary;
}

</style>
