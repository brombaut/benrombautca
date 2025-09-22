export enum PublicationLinkType {
  ResearchGate = "ResearchGate",
  ACM = "ACM",
  Queens = "Queen's",
  PDF = "PDF",
  Slides = "Slides",
  Forthcoming = "Forthcoming",
  CSER22 = "CSER '22",
  Arxiv = "Arxiv"
}

export interface PublicationLink {
  type: PublicationLinkType | string;
  url: string;
}

export enum PublicationType {
  Journal = "J",
  Conference = "C",
  Thesis = "T",
  Presentation = "P",
  Unpublished = "U",
}

export enum PublicationVenue {
  Forthcoming = "Forthcoming",
  TOSEM = "ACM Transactions on Software Engineering and Methodology (TOSEM)",
  TSE = "IEEE Transactions on Software Engineering (TSE)",
  EMSE = "Springer Empirical Software Engineering (EMSE)",
  Queens = "Queen's University",
  CSER = "Consortium for Software Engineering Research (CSER)",
  FSE = "Foundations of Software Engineering (FSE)",
  KDD = "Knowledge Discovery and Data Mining (KDD)",
  Unpublished = "Unpublished",
}

export interface Publication {
  type: PublicationType;
  title: string;
  authors: string | string[];
  venue: PublicationVenue | string;
  dateAccepted: Date;
  links: PublicationLink[];

  get year(): number;
  get month(): string;
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
    public venue: PublicationVenue | string,
    public dateAccepted: Date,
    public links: PublicationLink[],
  ) { }

  get year() {
    return this.dateAccepted.getFullYear();
  }

  get month() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December",
    ];
    return monthNames[this.dateAccepted.getMonth()];
  }
}

export class ThesisPublication implements Publication {
  type: PublicationType = PublicationType.Thesis;

  constructor(
    public title: string,
    public authors: string,
    public venue: PublicationVenue | string,
    public dateAccepted: Date,
    public links: PublicationLink[],
    public thesisType: string,
  ) { }

  get year() {
    return this.dateAccepted.getFullYear();
  }

  get month() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December",
    ];
    return monthNames[this.dateAccepted.getMonth()];
  }

}

export class PresentationPublication implements Publication {
  type: PublicationType = PublicationType.Presentation;

  constructor(
    public title: string,
    public authors: string[],
    public venue: PublicationVenue | string,
    public dateAccepted: Date,
    public links: PublicationLink[],
    public location: string,
  ) { }

  get year() {
    return this.dateAccepted.getFullYear();
  }

  get month() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December",
    ];
    return monthNames[this.dateAccepted.getMonth()];
  }

  get dayOfMonth() {
    return this.dateAccepted.getDate();
  }

}

export class UnpublishedPublication implements Publication {
  type: PublicationType = PublicationType.Unpublished;
  venue: PublicationVenue = PublicationVenue.Unpublished;

  constructor(
    public title: string,
    public authors: string[],
    public dateAccepted: Date,
    public links: PublicationLink[],
  ) { }

  get year() {
    return this.dateAccepted.getFullYear();
  }

  get month() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December",
    ];
    return monthNames[this.dateAccepted.getMonth()];
  }
}

export class ConferencePublication implements Publication {
  type: PublicationType = PublicationType.Conference;

  constructor(
    public title: string,
    public authors: string[],
    public venue: PublicationVenue | string,
    public dateAccepted: Date,
    public links: PublicationLink[],
    public conferenceName: string,
  ) { }

  get year() {
    return this.dateAccepted.getFullYear();
  }

  get month() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December",
    ];
    return monthNames[this.dateAccepted.getMonth()];
  }
}
