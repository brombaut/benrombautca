<template>
  <section id="blog">
    <SectionHeader
      title="Blog"
      icon="pen-square"
      subtext="A blog. Some things I've written." />
    <div class="section-body">
      <div v-for="group in postsByYear" :key="group.year" class="year-group">
        <div class="year-label">{{ group.year }}</div>
        <div
          v-for="post in group.posts"
          :key="post.id"
          class="post-row"
          role="button"
          tabindex="0"
          @click="postClicked(post)"
          @keydown.enter="postClicked(post)">
          <div class="post-title">{{ post.title }}</div>
          <div class="post-meta">
            <span class="post-date">{{ formatDate(post.createdAt) }}</span>
            <span v-if="post.description" class="post-description"> &middot; {{ post.description }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SectionHeader from "../shared/SectionHeader.vue";
import { BlogPostsProxy, BlogPost } from "./BlogPostsProxy";

interface YearGroup {
  year: number;
  posts: BlogPost[];
}

export default defineComponent({
  name: "BlogSection",
  components: {
    SectionHeader,
  },
  data() {
    return {
      blogPosts: new BlogPostsProxy().blogPosts as BlogPost[],
    };
  },
  computed: {
    postsToDisplay(): BlogPost[] {
      return this.blogPosts
        .filter((p: BlogPost) => p.show && !p.archived)
        .sort((a: BlogPost, b: BlogPost) => {
          return b.createdAt.getTime() - a.createdAt.getTime();
        });
    },
    postsByYear(): YearGroup[] {
      const groups: { [year: number]: BlogPost[] } = {};
      this.postsToDisplay.forEach((post: BlogPost) => {
        const year = post.createdAt.getUTCFullYear();
        if (!groups[year]) groups[year] = [];
        groups[year].push(post);
      });
      return Object.keys(groups)
        .map(Number)
        .sort((a, b) => b - a)
        .map(year => ({ year, posts: groups[year] }));
    },
  },
  methods: {
    postClicked(post: BlogPost) {
      this.$router.push({ name: "selectedBlogPost", params: { postId: post.id } });
    },
    formatDate(d: Date) {
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getUTCMonth()]} ${d.getUTCDate()}`;
    },
  },
});
</script>

<style lang="scss">
#blog {
  display: flex;
  flex-direction: column;

  .section-body {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .year-group {
    margin-bottom: 32px;
  }

  .year-label {
    font-size: 0.85em;
    font-weight: 700;
    color: $hFontColor;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding-bottom: 8px;
    border-bottom: 2px solid $secondaryDark;
    margin-bottom: 4px;
  }

  .post-row {
    padding: 14px 8px;
    border-bottom: 1px solid $secondaryDark;
    cursor: pointer;
    transition: background-color 0.1s;

    &:hover {
      background-color: $secondaryLight;

      .post-title {
        color: $primary;
      }
    }
  }

  .post-title {
    font-size: 1.05em;
    font-weight: 600;
    color: $fontColor;
    margin-bottom: 4px;
    line-height: 1.4;
  }

  .post-meta {
    font-size: 0.82em;
    color: $silver;
  }

  .post-description {
    font-style: italic;
  }
}
</style>
