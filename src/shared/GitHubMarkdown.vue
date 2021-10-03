<template>
  <div
    class="github-markdown-style"
    v-html="content" />
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "GitHubMarkdown",
  props: {
    content: String,
  },
  methods: {
    resizeSourceCodeEl(preCodeEl: HTMLPreElement): void {
      preCodeEl.style.width = "";
      setTimeout(() => {
        if (!preCodeEl.parentElement) return;
        const { width: parentWidth } = preCodeEl.parentElement.getBoundingClientRect();
        const oneSidePadding = 20;
        preCodeEl.style.width = `${parentWidth - (oneSidePadding * 2)}px`;
      }, 0);
    },
    resizeAllCodeEls() {
      const preCodeEls: NodeListOf<HTMLPreElement> = this.$el.querySelectorAll("pre.sourceCode");
      preCodeEls.forEach((preCodeEl: HTMLPreElement) => {
        this.resizeSourceCodeEl(preCodeEl);
      });
    },
  },
  mounted() {
    this.resizeAllCodeEls();
    window.addEventListener("resize", this.resizeAllCodeEls);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.resizeAllCodeEls);
  },
});
</script>

<style lang="scss">
@import "@/styles/github_article.scss";

</style>
