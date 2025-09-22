import { Publication, PublicationLinkType, JournalPublication, PublicationVenue, ThesisPublication, PresentationPublication, UnpublishedPublication, ConferencePublication } from "./types";

// Journal Publications
const journalPublications: JournalPublication[] = [
  new JournalPublication(
    "There's no such thing as a free lunch: Lessons learned from exploring the overhead introduced by the Greenkeeper dependency bot in npm",
    [
      "Benjamin Rombaut",
      "Filipe R. Cogo",
      "Bram Adams",
      "Ahmed E. Hassan",
    ],
    PublicationVenue.TOSEM,
    new Date(2022, 1, 24),
    [
      {
        type: PublicationLinkType.ACM,
        url: "https://dl.acm.org/doi/10.1145/3522587",
      },
      {
        type: PublicationLinkType.ResearchGate,
        url: "https://www.researchgate.net/publication/358911750_There's_no_such_thing_as_a_free_lunch_Lessons_learned_from_exploring_the_overhead_introduced_by_the_Greenkeeper_dependency_bot_in_npm",
      },
      {
        type: PublicationLinkType.PDF,
        url: "publications/Rombaut_Benjamin_J_202202_GreenkeeperOverhead.pdf",
      },
    ],
  ),
];

// Thesis Publications
const thesisPublications: ThesisPublication[] = [
  new ThesisPublication(
    "Studying the overhead and crowd-sourced risk assessment strategy of dependency management bots",
    "Benjamin Rombaut",
    PublicationVenue.Queens,
    new Date(2022, 4, 19),
    [
      {
        type: PublicationLinkType.Queens,
        url: "https://qspace.library.queensu.ca/handle/1974/30136",
      },
      {
        type: PublicationLinkType.PDF,
        url: "publications/Rombaut_Benjamin_J_202205_MSc.pdf",
      },
    ],
    "Master's Thesis",
  ),
];

// Presentation Publications
const presentationPublications: PresentationPublication[] = [
  new PresentationPublication(
    "Lessons learned from exploring the overhead introduced by the Greenkeeper dependency bot",
    ["Benjamin Rombaut"],
    PublicationVenue.CSER,
    new Date(2022, 4, 30),
    [
      {
        type: PublicationLinkType.CSER22,
        url: "https://www.cser.ca/2022s",
      },
      {
        type: PublicationLinkType.Slides,
        url: "publications/Rombaut_Benjamin_J_202205_GreenkeeperOverhead_Presentation_CSER2022.pdf",
      },
    ],
    "Montreal, Canada",
  ),
  new PresentationPublication(
    "AIware Observability",
    ["Benjamin Rombaut"],
    "AIware Leadership Bootcamp (2024) & AIware Mini Bootcamp (co-located with ICSE 2025)",
    new Date(2024, 10, 8),
    [
      {
        type: "AIWare Leadership Bootcamp 2024",
        url: "https://www.aiwarebootcamp.io/",
      },
      {
        type: "AIWare Mini Bootcamp 2025",
        url: "https://www.aiwarebootcamp.io/mini.html",
      },
      {
        type: PublicationLinkType.Slides,
        url: "publications/202411_aiware_bootcamp_observability_for_pdf.pdf",
      },
      {
        type: "Video",
        url: "https://www.youtube.com/watch?v=gXsZgtyJ3s8",
      },
    ],
    "Toronto, Canada & Ottawa, Canada",
  ),
  new PresentationPublication(
    "Prompting with DSPy - Hands On Tutorial",
    ["Benjamin Rombaut"],
    "AIware Leadership Bootcamp (2024)",
    new Date(2024, 10, 6),
    [
      {
        type: "AIWare Leadership Bootcamp 2024",
        url: "https://www.aiwarebootcamp.io/",
      },
      {
        type: "Video",
        url: "https://www.youtube.com/watch?v=ZoEEMVlMavY",
      },
    ],
    "Toronto, Canada",
  ),
];

// Unpublished Publications
const unpublishedPublications: UnpublishedPublication[] = [
  new UnpublishedPublication(
    "Leveraging the crowd for dependency management: An empirical study on the Dependabot compatibility score",
    [
      "Benjamin Rombaut",
      "Filipe R. Cogo",
      "Ahmed E. Hassan",
    ],
    new Date(2022, 2, 1),
    [
      {
        type: PublicationLinkType.Arxiv,
        url: "https://arxiv.org/abs/2403.09012",
      },
      {
        type: PublicationLinkType.PDF,
        url: "publications/Rombaut_Benjamin_J_202203_DependabotCompatibilityScore.pdf",
      },
    ],
  ),
  new UnpublishedPublication(
    "An Empirical Study of Library Usage and Dependency in Deep Learning Frameworks",
    [
      "Mohamed Raed El aoun",
      "Lionel Nganyewou Tidjon",
      "Benjamin Rombaut",
      "Foutse Khomh",
      "Ahmed E. Hassan"
    ],
    new Date(2022, 10, 28),
    [
      {
        type: PublicationLinkType.Arxiv,
        url: "https://arxiv.org/abs/2211.15733",
      },
    ],
  ),
  new UnpublishedPublication(
    "Watson: A Cognitive Observability Framework for the Reasoning of LLM-Powered Agents",
    [
      "Benjamin Rombaut",
      "Sogol Masoumzadeh",
      "Kirill Vasilevski",
      "Dayi Lin",
      "Ahmed E. Hassan"
    ],
    new Date(2024, 10, 5),
    [
      {
        type: PublicationLinkType.Arxiv,
        url: "https://www.arxiv.org/abs/2411.03455",
      },
      {
        type: PublicationLinkType.PDF,
        url: "publications/202505_agent_observability_ase2025.pdf",
      },
    ],
  ),
];

// Placeholder Conference Publication
const conferencePublications: ConferencePublication[] = [
  new ConferencePublication(
    "A Tutorial on Software Engineering for FMware",
    [
      "Filipe R. Cogo",
      "Gopi Krishnan Rajbahadur",
      "Dayi Lin",
      "Keheliya Gallaba",
      "Benjamin Rombaut",
      "Gustavo Oliva",
      "Jiahuei (Justina) Lin",
      "Kirill Vasilevski",
      "Ahmed E. Hassan",
    ],
    PublicationVenue.FSE,
    new Date(2025, 6, 28),
    [
      {
        type: PublicationLinkType.ACM,
        url: "https://dl.acm.org/doi/abs/10.1145/3696630.3728621",
      },
    ],
    "FSE Companion '25: Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineerin",
  ),
  new ConferencePublication(
    "The Hitchhikers Guide to Production-ready Trustworthy Foundation Model powered Software (FMware)",
    [
      "Kirill Vasilevski",
      "Gopi Krishnan Rajbahadur",
      "Gustavo A. Oliva",
      "Benjamin Rombaut",
      "Keheliya Gallaba",
      "Filipe R. Cogo",
      "Jiahuei (Justina) Lin",
      "Dayi Lin",
      "Haoxiang Zhang",
      "Bouyan Chen",
      "Kishanthan Thangarajah",
      "Ahmed E. Hassan",
      "Zhen Ming (Jack) Jiang",
    ],
    "Placeholder Venue",
    new Date(2025, 7, 3),
    [
      {
        type: PublicationLinkType.ACM,
        url: "https://dl.acm.org/doi/10.1145/3711896.3736572",
      },
      {
        type: PublicationLinkType.Arxiv,
        url: "https://arxiv.org/abs/2505.10640",
      },
      {
        type: PublicationLinkType.PDF,
        url: "publications/202505_hitchhikers_guide_fmware.pdf",
      },
    ],
    "KDD '25: Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2",
  ),
];

// Combine all publications
const publications: Publication[] = [
  ...journalPublications,
  ...thesisPublications,
  ...presentationPublications,
  ...unpublishedPublications,
  ...conferencePublications,
];


export default publications;
