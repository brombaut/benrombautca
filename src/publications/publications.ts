import { Publication, PublicationLinkType, JournalPublication, PublicationVenue, ThesisPublication, PresentationPublication, UnpublishedPublication } from "./types";

const publications: Publication[] = [
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
    ],
    "Montreal, QC, Canada",
  ),
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
        type: PublicationLinkType.PDF,
        url: "publications/Rombaut_Benjamin_J_202203_DependabotCompatibilityScore.pdf",
      },
    ],
  ),
];

export default publications;
