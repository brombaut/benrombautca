<template>
    <nav id='navbar'>
        <NavBarIconHighlight />
        <div class='icons-section top-icons'>
            <NavBarIcon class='top-icon' iconStyle="fas" iconName="home"/>
        </div>
        <div class='icons-section middle-icons'>
            <NavBarIcon iconStyle="fas" iconName="street-view"/>
            <NavBarIcon iconStyle="far" iconName="folder-open"/>
            <NavBarIcon iconStyle="far" iconName="map"/>
            <NavBarIcon iconStyle="far" iconName="envelope"/>
        </div>
        <div class='icons-section bottom-icons'>
            <NavBarIcon iconStyle="fab" iconName="github"/>
            <NavBarIcon iconStyle="fab" iconName="linkedin"/>
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
    mounted() {
        const firstIconEl = document.querySelector('.top-icon');
        if (firstIconEl) {
            bus.$emit('navIconClicked', firstIconEl.getBoundingClientRect());
        }
    },
};
</script>

<style lang='scss'>
nav {
    width: 100px;
    height: auto;
    background-color: darken(#1c1d25, 5%);
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
