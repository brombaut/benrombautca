import aaMetas from "./authored_articles_meta.json";
import aaContent from "./authored_articles_content.json";

interface AuthoredArticleContent {
  _id: string;
  _body: string;
}

interface AuthoredArticleMeta {
  _id: string;
  _title: string,
  _createdAt: Date,
  _description: string,
  _show: boolean,
  _archived: boolean
}

export interface AuthoredArticle {
  readonly id: string,
  readonly title: string,
  readonly createdAt: Date,
  readonly description: string,
  readonly body: string,
  readonly show: boolean,
  readonly archived: boolean
}

export class AuthoredArticlesProxy {
  private _aaMetas: AuthoredArticleMeta[];
  private _aaContents: AuthoredArticleContent[];
  private _authoredArticles: AuthoredArticle[];

  constructor() {
    this._aaMetas = aaMetas as unknown as AuthoredArticleMeta[];
    this._aaContents = aaContent as unknown as AuthoredArticleContent[];
    this._authoredArticles = [];
    this.buildAAs();
  }

  get authoredArticles() {
    return this._authoredArticles;
  }

  private buildAAs() {
    const merged: (AuthoredArticleMeta | AuthoredArticleContent)[] = [];
    this._aaMetas.forEach((meta: AuthoredArticleMeta) => {
      const body: string = this._aaContents.find((aac: AuthoredArticleContent) => aac._id === meta._id)?._body || "";
      merged.push({
        ...meta,
        _body: body,
      });
    });
    const mapper = (dto: any): AuthoredArticle => {
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
    this._authoredArticles = merged.map(mapper);
  }

}
