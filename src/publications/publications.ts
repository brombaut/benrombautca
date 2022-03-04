import { Publication, PublicationType, PublicationLinkType, JournalPublication, PublicationVenue, ThesisPublication } from "./types";

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
        type: PublicationLinkType.ResearchGate,
        url: "https://www.researchgate.net/publication/358911750_There's_no_such_thing_as_a_free_lunch_Lessons_learned_from_exploring_the_overhead_introduced_by_the_Greenkeeper_dependency_bot_in_npm",
      },
    ],
  ),
  new JournalPublication(
    "Leveraging the crowd for dependency management: An empirical study on the Dependabot compatibility score",
    [
      "Benjamin Rombaut",
      "Filipe R. Cogo",
      "Ahmed E. Hassan",
    ],
    PublicationVenue.TSE,
    new Date(),
    [],
  ),
  new ThesisPublication(
    "Studying the use of bots for supporting dependency management",
    "Benjamin Rombaut",
    PublicationVenue.Queens,
    new Date(),
    [],
    "Master's thesis",
  ),
];

export default publications;
