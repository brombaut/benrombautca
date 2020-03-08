<template>
  <div id='nav-icon-highlight'>
  </div>
</template>

<script>
import { bus } from '@/main';

export default {
    name: 'IconHighlight',
    mounted() {
        bus.$on('setNavIconHighlight', this.updateNacIconHighlightPosition);
    },
    methods: {
        updateNacIconHighlightPosition(boundingClientRect) {
            const highlightEl = document.querySelector('#nav-icon-highlight');
            if (highlightEl) {
                highlightEl.style.top = `${boundingClientRect.y}px`;
                highlightEl.style.left = `${boundingClientRect.x}px`;
                highlightEl.style.width = `${boundingClientRect.width}px`;
                highlightEl.style.height = `${boundingClientRect.height}px`;
            }
        },
    },
};
</script>

<style lang='scss'>
#nav-icon-highlight {
    position: absolute;
    border-radius: 8px;;
    background-color: lighten(#1c1d25, 3%);
    transition: 0.3s;
    widyj: 60px;
    height: 60px;

}
</style>
