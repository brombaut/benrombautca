export enum PublicationLinkType {
  ResearchGate = 1,
  Queens,
}

export interface PublicationLink {
  type: PublicationLinkType;
  url: string;
}

export enum PublicationType {
  Journal = "J",
  Conference = "C",
  Thesis = "T",
}

export enum PublicationVenue {
  TOSEM = "ACM Transactions on Software Engineering and Methodology (TOSEM)",
  Queens = "Queen's University"
}

export interface Publication {
  type: PublicationType;
  title: string;
  authors: string | string[];
  venue: PublicationVenue;
  dateAccepted: Date;
  links: PublicationLink[];
}

export interface ViewPublication {
  type: PublicationType,
  header: string,
  items: Publication[],
}

export class JournalPublication implements Publication {
  type: PublicationType = PublicationType.Journal;

  constructor(
    public title: string,
    public authors: string[],
    public venue: PublicationVenue,
    public dateAccepted: Date,
    public links: PublicationLink[],
  ) { }

  get year() {
    return this.dateAccepted.getFullYear();
  }
}

export class ThesisPublication implements Publication {
  type: PublicationType = PublicationType.Thesis;

  constructor(
    public title: string,
    public authors: string,
    public venue: PublicationVenue,
    public dateAccepted: Date,
    public links: PublicationLink[],
    public thesisType: string,
  ) { }

  get year() {
    return this.dateAccepted.getFullYear();
  }

}
