<template>
  <section id="blog">
    <SectionHeader
      title="Blog"
      icon="pen-square"
      subtext="Writings about some things I've done" />
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
          <div class="post-top">
            <span v-if="post.series" class="post-series">
              {{ post.series.name }} <span class="post-series-part">&middot; Part {{ post.series.part }}</span>
            </span>
            <span class="post-date">{{ formatDate(post.createdAt) }}</span>
          </div>
          <h3 class="post-title">
            <span class="post-emoji" aria-hidden="true">{{ post.emoji }}</span>
            {{ post.displayTitle }}
          </h3>
          <p v-if="post.description" class="post-description">{{ post.description }}</p>
          <div class="post-footer">
            <span class="post-reading-time">{{ post.readingMinutes }} min read</span>
            <span class="post-read-more">Read post &rarr;</span>
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

  .section-header .section-header_content {
    font-size: 2rem;
  }

  .section-header > p {
    font-size: 1.15rem;
  }

  .section-body {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .year-group {
    margin-bottom: 40px;
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
    padding: 28px 20px 26px 20px;
    border-bottom: 1px solid $secondaryDark;
    border-left: 3px solid transparent;
    text-align: left;
    cursor: pointer;
    transition: background-color 0.15s, border-left-color 0.15s;

    &:hover,
    &:focus-visible {
      background-color: $secondaryLight;
      border-left-color: $primary;
      outline: none;

      .post-title {
        color: $primary;
      }

      .post-read-more {
        opacity: 1;
      }
    }
  }

  .post-top {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 10px;
    font-size: 0.78em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .post-series {
    font-weight: 700;
    color: $primaryDark;
  }

  .post-series-part {
    font-weight: 600;
    color: $onyx;
    opacity: 0.75;
  }

  .post-date {
    margin-left: auto;
    color: $onyx;
    opacity: 0.75;
    white-space: nowrap;
  }

  .post-title {
    font-size: 1.5em;
    font-weight: 600;
    color: $fontColor;
    margin: 0 0 10px 0;
    line-height: 1.3;
    transition: color 0.15s;
  }

  .post-emoji {
    margin-right: 6px;
    font-size: 0.95em;
    // Emoji shouldn't shift with the title colour on hover
    color: initial;
  }

  .post-description {
    margin: 0;
    max-width: 68ch;
    font-size: 1em;
    line-height: 1.65;
    color: $onyx;
  }

  .post-footer {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    gap: 12px;
    margin-top: 14px;
    font-size: 0.82em;
    color: $onyx;
    opacity: 0.85;
  }

  .post-read-more {
    margin-left: auto;
    color: $primary;
    font-weight: 600;
    opacity: 0;
    transition: opacity 0.15s;
    white-space: nowrap;
  }
}

@media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
  #blog {
    .post-row {
      padding: 20px 12px 18px 12px;
    }

    .post-title {
      font-size: 1.25em;
    }

    .post-description {
      font-size: 0.92em;
    }

    .post-read-more {
      display: none;
    }
  }
}
</style>
