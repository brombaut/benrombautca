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
            showConnectors: true,
        };
    },
    watch: {
        showConnectors(newVal) {
            bus.$emit('emitConnectorsVisible', newVal);
        },
    },
    methods: {
        handleViewChanged(clickedIconName) {
            this.currView = clickedIconName;
            this.checkWindowWidth();
        },
        handleWindowResize(e) {
            const windowWidth = e.target.innerWidth;
            if (this.showConnectors && windowWidth < 1100) {
                this.showConnectors = false;
            } else if (!this.showConnectors && windowWidth >= 1350) {
                this.showConnectors = true;
            }
        },
        checkWindowWidth() {
            if (window.innerWidth < 1100) {
                this.showConnectors = false;
            }
        },
    },
    mounted() {
        bus.$on('navIconClicked', this.handleViewChanged);
        window.addEventListener('resize', this.handleWindowResize);
        this.checkWindowWidth();
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.handleWindowResize);
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
    margin-top: 48px;
    z-index: 1;
    // -webkit-text-stroke: 1px black;
    font-size: 50px;
}

</style>
