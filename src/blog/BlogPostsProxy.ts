import blogPostsMeta from "./blog_posts_meta.json";
import blogPostsContent from "./blog_posts_content.json";

interface BlogPostContent {
  _id: string;
  _body: string;
}

interface BlogPostMeta {
  _id: string;
  _title: string,
  _createdAt: Date,
  _description: string,
  _show: boolean,
  _archived: boolean
}

export interface BlogPostSeries {
  readonly name: string,
  readonly part: number
}

export interface BlogPost {
  readonly id: string,
  readonly title: string,
  readonly createdAt: Date,
  readonly description: string,
  readonly body: string,
  readonly show: boolean,
  readonly archived: boolean,
  // Derived: the series a post belongs to, parsed from a "[Series N] " title prefix
  readonly series: BlogPostSeries | null,
  // Derived: the title with any series prefix removed
  readonly displayTitle: string,
  // Derived: estimated reading time in minutes, from the body word count
  readonly readingMinutes: number,
  // Derived: icon shown before the title, shared by every post in a series
  readonly emoji: string
}

const SERIES_PREFIX = /^\[(.+?)\s+(\d+)\]\s*/;
const WORDS_PER_MINUTE = 225;

// Every post in a series shares its series icon
const SERIES_EMOJI: { [name: string]: string } = {
  "AI Experience": "🧭",
  "AI Slop": "🧹",
  "SWE-bench Architecture": "🏗️",
  "Learning LLMs": "🧠",
};

// One-off posts that aren't part of a series can opt into their own icon
const POST_EMOJI: { [id: string]: string } = {
  "20260710_aiware_observability": "🔭",
  "coding-agent-architectures": "🤖",
};

const DEFAULT_EMOJI = "📝";

function parseSeries(title: string): BlogPostSeries | null {
  const match = title.match(SERIES_PREFIX);
  if (!match) return null;
  return { name: match[1], part: Number(match[2]) };
}

function stripSeries(title: string): string {
  return title.replace(SERIES_PREFIX, "");
}

function emojiFor(id: string, series: BlogPostSeries | null): string {
  if (series && SERIES_EMOJI[series.name]) return SERIES_EMOJI[series.name];
  return POST_EMOJI[id] || DEFAULT_EMOJI;
}

function readingMinutes(body: string): number {
  const words = body.replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / WORDS_PER_MINUTE));
}

export class BlogPostsProxy {
  private _blogPostsMeta: BlogPostMeta[];
  private _blogPostsContent: BlogPostContent[];
  private _blogPosts: BlogPost[];

  constructor() {
    this._blogPostsMeta = blogPostsMeta as unknown as BlogPostMeta[];
    this._blogPostsContent = blogPostsContent as unknown as BlogPostContent[];
    this._blogPosts = [];
    this.buildBlogPosts();
  }

  get blogPosts() {
    return this._blogPosts;
  }

  private buildBlogPosts() {
    const merged: (BlogPostMeta | BlogPostContent)[] = [];
    this._blogPostsMeta.forEach((meta: BlogPostMeta) => {
      const body: string = this._blogPostsContent.find((bpc: BlogPostContent) => bpc._id === meta._id)?._body || "";
      merged.push({
        ...meta,
        _body: body,
      });
    });
    const mapper = (dto: any): BlogPost => {
      const series = parseSeries(dto._title);
      return {
        id: dto._id,
        title: dto._title,
        createdAt: new Date(dto._createdAt),
        description: dto._description,
        body: dto._body,
        show: dto._show,
        archived: dto._archived,
        series,
        displayTitle: stripSeries(dto._title),
        readingMinutes: readingMinutes(dto._body),
        emoji: emojiFor(dto._id, series),
      };
    };
    this._blogPosts = merged.map(mapper);
  }

}
