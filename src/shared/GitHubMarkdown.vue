<template>
  <div
    class="github-markdown-style"
    v-html="content" />
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class GitHubMarkdown extends Vue {

  @Prop()
  content!: string;

  resizeSourceCodeEl(preCodeEl: HTMLPreElement): void {
    preCodeEl.style.width = "";
    setTimeout(() => {
      if (!preCodeEl.parentElement) return;
      const { width: parentWidth } = preCodeEl.parentElement.getBoundingClientRect();
      const oneSidePadding = 20;
      preCodeEl.style.width = `${parentWidth - (oneSidePadding * 2)}px`;
    }, 0);
  }

  resizeAllCodeEls() {
    const preCodeEls: NodeListOf<HTMLPreElement> = this.$el.querySelectorAll("pre.sourceCode");
    preCodeEls.forEach((preCodeEl: HTMLPreElement) => {
      this.resizeSourceCodeEl(preCodeEl);
    });
  }

  mounted() {
    this.resizeAllCodeEls();
    window.addEventListener("resize", this.resizeAllCodeEls);
  }

  beforeUnmount() {
    window.removeEventListener("resize", this.resizeAllCodeEls);
  }

}
</script>

<style lang="scss">
@import "@/styles/github_article.scss";

</style>
