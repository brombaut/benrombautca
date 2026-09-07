<template>
  <section id="selected-article">
    <div v-if="selectedPost.series" class="post-series">
      {{ selectedPost.series.name }} <span class="post-series-part">&middot; Part {{ selectedPost.series.part }}</span>
    </div>
    <SectionHeader :title="selectedPost.displayTitle" icon="" :subtext="selectedPost.description" />
    <div class="meta-container">
      <div class="dates">
        Created {{ formatDate(selectedPost.createdAt) }}
        &middot; {{ selectedPost.readingMinutes }} min read
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
      return `${months[d.getUTCMonth()]} ${d.getUTCDate()}, ${d.getUTCFullYear()}`;
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

  .post-series {
    margin-bottom: 4px;
    font-size: 0.85em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: $primaryDark;

    .post-series-part {
      font-weight: 600;
      color: $onyx;
      opacity: 0.75;
    }
  }

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
