class ExternalProfile {
  private _id: string;
  private _icon: string[];
  private _url: string;

  constructor(id: string, icon: string[], url: string) {
    this._id = id;
    this._icon = icon;
    this._url = url;
  }

  id(): string {
    return this._id;
  }

  icon(): string[] {
    return this._icon;
  }

  url(): string {
    return this._url;
  }
}

export default ExternalProfile;
