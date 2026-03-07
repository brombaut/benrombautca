<template>
  <section id="selected-article">
    <SectionHeader :title="selectedPost.title" icon="" :subtext="selectedPost.description" />
    <div class="meta-container">
      <div class="dates">
        Created {{ formatDate(selectedPost.createdAt) }}
      </div>
    </div>
    <div class="section-body">
      <GitHubMarkdown :content="selectedPost.body" />
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import GitHubMarkdown from "../shared/GitHubMarkdown.vue";
import { BlogPostsProxy, BlogPost } from "./BlogPostsProxy";

export default defineComponent({
  name: "SelectedBlogPostSection",
  components: {
    SectionHeader,
    GitHubMarkdown,
  },
  data() {
    return {
      selectedPostId: "",
      selectedPost: {} as BlogPost,
    };
  },
  methods: {
    loadSelectedPost(postId: string): BlogPost | null {
      const allPosts: BlogPost[] = new BlogPostsProxy().blogPosts;
      const selectedPost: BlogPost | undefined = allPosts.find(
        (p: BlogPost) => p.id === postId,
      );
      return selectedPost || null;
    },
    formatDate(d: Date) {
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
    },
    backToBlog() {
      this.$router.push({ name: "blog" });
    },
  },
  created() {
    window.scrollTo(0, 0);
    this.selectedPostId = this.$router.currentRoute.value.params.postId as string;
    const loadedPost: BlogPost | null = this.loadSelectedPost(
      this.selectedPostId,
    );
    if (loadedPost) {
      this.selectedPost = loadedPost;
    }
  },
});
</script>

<style lang="scss">
#selected-article {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  .section-header {
    margin-bottom: 4px;

    .section-title {
      line-height: 1.5em;
    }
  }

  .meta-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 16px;

    .dates {
      margin: 0px 0;
    }

  }

  .section-body {
    text-align: left;
    width: 100%;
  }
}

</style>
