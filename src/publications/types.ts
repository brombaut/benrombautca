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

export interface ViewPublication {
  type: any,
  header: string,
  subHeader: string,
  items: Publication[],
}

export class Publication {
  constructor(
    public title: string,
    public authors: string[],
    public venue: string,
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
