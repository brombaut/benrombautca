<template>
    <nav id='navbar'>
        <NavBarIconHighlight />
        <div class='icons-section top-icons'>
            <NavBarIcon
                v-for="icon in topIcons"
                :key="icon.name"
                :icon="icon"
                :class='icon.classString' />
        </div>
        <div class='icons-section middle-icons'>
            <NavBarIcon
                v-for="icon in middleIcons"
                :key="icon.name"
                :icon="icon"/>
        </div>
        <div class='icons-section bottom-icons'>
            <NavBarIcon
                v-for="icon in bottomIcons"
                :key="icon.name"
                :icon="icon"/>
        </div>
    </nav>
</template>

<script>
import NavBarIcon from '@/components/NavBar/NavBarIcon.vue';
import NavBarIconHighlight from '@/components/NavBar/NavBarIconHighlight.vue';
import { bus } from '@/main';

export default {
    name: 'NavBar',
    components: {
        NavBarIcon,
        NavBarIconHighlight,
    },
    data() {
        const emitHighlightPosition = function(boundingRect, iconName) {
            bus.$emit('setNavIconHighlight', boundingRect);
            bus.$emit('navIconClicked', iconName);
        };
        const topIcons = [
            {
                name: 'home',
                hoverText: 'Home',
                iconStyle: 'fas',
                iconName: 'microchip',
                classString: 'top-icon',
                iconClickCallback: emitHighlightPosition,
            },
        ];
        const middleIcons = [
            {
                name: 'aboutMe',
                hoverText: 'About Me',
                iconStyle: 'fas',
                iconName: 'street-view',
                classString: '',
                iconClickCallback: emitHighlightPosition,
            },
            {
                name: 'portfolio',
                hoverText: 'Projects',
                iconStyle: 'far',
                iconName: 'folder-open',
                classString: '',
                iconClickCallback: emitHighlightPosition,
            },
            {
                name: 'recentActivity',
                hoverText: 'What I\'ve been up to',
                iconStyle: 'far',
                iconName: 'map',
                classString: '',
                iconClickCallback: emitHighlightPosition,
            },
            // {
            //     name: 'contactMe',
            //     hoverText: 'Contact Me',
            //     iconStyle: 'far',
            //     iconName: 'envelope',
            //     classString: '',
            //     iconClickCallback: emitHighlightPosition,
            // },
        ];
        const openGithub = function() {
            window.open('https://github.com/brombaut', '_blank').focus();
        };
        const openLinkedIn = function() {
            window.open('https://www.linkedin.com/in/benjamin-rombaut/', '_blank').focus();
        };
        const bottomIcons = [
            {
                name: 'github',
                hoverText: 'Github',
                iconStyle: 'fab',
                iconName: 'github',
                classString: '',
                iconClickCallback: openGithub,
                url: 'https://github.com/brombaut',
            },
            {
                name: 'linkedin',
                hoverText: 'LinkedIn',
                iconStyle: 'fab',
                iconName: 'linkedin',
                classString: '',
                iconClickCallback: openLinkedIn,
                url: 'https://www.linkedin.com/in/benjamin-rombaut/',
            },
        ];
        return {
            topIcons,
            middleIcons,
            bottomIcons,
        };
    },
    mounted() {
        const firstIconEl = document.querySelector('.top-icon');
        if (firstIconEl) {
            bus.$emit('setNavIconHighlight', firstIconEl.getBoundingClientRect());
            bus.$emit('navIconClicked', 'home');
        }
    },
};
</script>

<style lang='scss'>
nav {
    width: 100px;
    min-width: 100px;
    height: auto;
    background-color: $secondaryDark;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 24px 0;
    position: relative;

    .icons-section  {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
}

</style>
