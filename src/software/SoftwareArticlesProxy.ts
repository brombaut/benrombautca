import saMetas from "./software_articles_meta.json";
import saContent from "./software_articles_content.json";

interface SoftwareArticleContent {
  _id: string;
  _body: string;
}

interface SoftwareArticleMeta {
  _id: string;
  _title: string,
  _createdAt: Date,
  _updatedAt: Date,
  _description: string,
  _show: boolean,
  _order: number,
  _externalRepos: ExternalRepo[];
  _techUsed: Tech[];
}

export interface ExternalRepo {
  _id: string;
  _imagePath: string;
  _url: string;
  _title: string;
  _hoverText: string;
}

export interface Tech {
  _id: string;
  _imagePath: string;
  _title: string;
  _hoverText: string;
}

export interface SoftwareArticle {
  readonly id: string;
  readonly title: string;
  readonly createdAt: Date;
  readonly updatedAt: Date;
  readonly description: string;
  readonly body: string;
  readonly show: boolean;
  readonly order: number;
  readonly externalRepos: ExternalRepo[];
  readonly techUsed: Tech[];
}

export class SoftwareArticlesProxy {
  private _saMetas: SoftwareArticleMeta[];
  private _saContents: SoftwareArticleContent[];
  private _softwareArticles: SoftwareArticle[];

  constructor() {
    this._saMetas = saMetas as unknown as SoftwareArticleMeta[];
    this._saContents = saContent as unknown as SoftwareArticleContent[];
    this._softwareArticles = [];
    this.buildSAs();
  }

  get softwareArticles() {
    return this._softwareArticles;
  }

  private buildSAs() {
    const merged: (SoftwareArticleMeta | SoftwareArticleContent)[] = [];
    this._saMetas.forEach((meta: SoftwareArticleMeta) => {
      const body: string = this._saContents.find((sac: SoftwareArticleContent) => sac._id === meta._id)?._body || "";
      merged.push({
        ...meta,
        _body: body,
      });
    });
    const mapper = (dto: any): SoftwareArticle => {
      return {
        id: dto._id,
        title: dto._title,
        createdAt: new Date(dto._createdAt),
        updatedAt: new Date(dto._updatedAt),
        description: dto._description,
        body: dto._body,
        show: dto._show,
        order: dto._order,
        externalRepos: dto._externalRepos,
        techUsed: dto._techUsed,
      };
    };
    this._softwareArticles = merged.map(mapper);
  }

}
