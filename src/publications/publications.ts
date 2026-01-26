import { Publication, PublicationLinkType } from "./types";

// All Publications
const publications: Publication[] = [
  new Publication(
    "There's no such thing as a free lunch: Lessons learned from exploring the overhead introduced by the Greenkeeper dependency bot in npm",
    [
      "Benjamin Rombaut",
      "Filipe R. Cogo",
      "Bram Adams",
      "Ahmed E. Hassan",
    ],
    "ACM Transactions on Software Engineering and Methodology (TOSEM)",
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

  new Publication(
    "Studying the overhead and crowd-sourced risk assessment strategy of dependency management bots",
    ["Benjamin Rombaut"],
    "Queen's University, Master's Thesis",
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
  ),

  new Publication(
    "Lessons learned from exploring the overhead introduced by the Greenkeeper dependency bot",
    ["Benjamin Rombaut"],
    "Consortium for Software Engineering Research (CSER), Montreal, Canada",
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
  ),
  new Publication(
    "AIware Observability",
    ["Benjamin Rombaut"],
    "AIware Leadership Bootcamp 2024 & Mini Bootcamp 2025",
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
  ),
  new Publication(
    "Prompting with DSPy - Hands On Tutorial",
    ["Benjamin Rombaut"],
    "AIware Leadership Bootcamp 2024",
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
  ),

  new Publication(
    "Leveraging the crowd for dependency management: An empirical study on the Dependabot compatibility score",
    [
      "Benjamin Rombaut",
      "Filipe R. Cogo",
      "Ahmed E. Hassan",
    ],
    "Unpublished",
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
  new Publication(
    "An Empirical Study of Library Usage and Dependency in Deep Learning Frameworks",
    [
      "Mohamed Raed El aoun",
      "Lionel Nganyewou Tidjon",
      "Benjamin Rombaut",
      "Foutse Khomh",
      "Ahmed E. Hassan",
    ],
    "Unpublished",
    new Date(2022, 10, 28),
    [
      {
        type: PublicationLinkType.Arxiv,
        url: "https://arxiv.org/abs/2211.15733",
      },
    ],
  ),

  new Publication(
    "Watson: A Cognitive Observability Framework for the Reasoning of LLM-Powered Agents",
    [
      "Benjamin Rombaut",
      "Sogol Masoumzadeh",
      "Kirill Vasilevski",
      "Dayi Lin",
      "Ahmed E. Hassan",
    ],
    "Automated Software Engineering (ASE) '25",
    new Date(2025, 10, 1),
    [
      {
        type: "ASE '25",
        url: "https://conf.researchr.org/details/ase-2025/ase-2025-papers/148/Watson-A-Cognitive-Observability-Framework-for-the-Reasoning-of-LLM-Powered-Agents",
      },
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
  new Publication(
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
    "Foundations of Software Engineering (FSE) Companion '25",
    new Date(2025, 6, 28),
    [
      {
        type: PublicationLinkType.ACM,
        url: "https://dl.acm.org/doi/abs/10.1145/3696630.3728621",
      },
    ],
  ),
  new Publication(
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
    "Knowledge Discovery and Data Mining (KDD) '25",
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
  ),
  new Publication(
    "From Vibe to Verifiable Spec-Driven Development: A Demo of Intent and Realization Engineering",
    [
      "Keheliya Gallaba",
      "Zhiyu Fan",
      "Jiahuei (Justina) Lin",
      "Filipe R. Cogo",
      "Benjamin Rombaut",
      "Dayi Lin",
      "Ahmed E. Hassan",
    ],
    "AAAI Workshop on Next-Gen Code Development with Collaborative AI Agents '26",
    new Date(2026, 1, 1),
    [],
  ),
];

export default publications;
