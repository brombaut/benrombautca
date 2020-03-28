<template>
    <div id='recent-activity'>
        <div class='scroll-container'>
            <h1>What I've Been Up To</h1>
            <div class='content-container'>
                <Books />
            </div>
        </div>
    </div>
</template>

<script>
import Books from '@/components/RecentActivity/Books.vue';

export default {
    name: 'RecentActivity',
    components: {
        Books,
    },
};
</script>

<style lang='scss'>
#recent-activity {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-x: auto;
    position: relative;

    .scroll-container {
        z-index: 1;
        // overflow-x: auto;

    }
}

</style>
