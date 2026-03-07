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

export interface BlogPost {
  readonly id: string,
  readonly title: string,
  readonly createdAt: Date,
  readonly description: string,
  readonly body: string,
  readonly show: boolean,
  readonly archived: boolean
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
      return {
        id: dto._id,
        title: dto._title,
        createdAt: new Date(dto._createdAt),
        description: dto._description,
        body: dto._body,
        show: dto._show,
        archived: dto._archived,
      };
    };
    this._blogPosts = merged.map(mapper);
  }

}
