import { Project } from "@/projects/project";

const sortProjects = function (a: Project, b: Project) {
  if (a.id < b.id) return -1;
  return 1;
};

const projects: Project[] = [
  {
    id: 1,
    name: "NHL API Frontend",
    description: "Web app to consume the publicly accessible portions of the NHL API.",
    techUsed: [
      "TypeScript",
      "Vue",
      "Vuex"
    ],
    url: "https://brombaut.github.io/nhl-api-frontend/#/",
    sourceUrl: "https://github.com/brombaut/nhl-api-frontend",
    thumbnail: "NhlApiFrontend.png",
    inProgress: false
  },
  {
    id: 2,
    name: "BEC Article Tracker",
    description: "A tool I built to keep track of tech-related articles I have read and articles I would like to read.",
    techUsed: [
      "Vue",
      "Firebase"
    ],
    url: "https://brombaut.github.io/article-tracker/",
    sourceUrl: "https://github.com/brombaut/article-tracker",
    thumbnail: "BecArticleTracker.png",
    inProgress: false
  },
  {
    id: 3,
    name: "Stack Overflow Question Scraper",
    description: "A site that allows users to quickly build queries for questions and view summaries of these questions on Stack Overflow.",
    techUsed: [
      "Vue",
      "Cheerio"
    ],
    url: "https://brombaut.github.io/stack-overflow-question-scraper/",
    sourceUrl: "https://github.com/brombaut/stack-overflow-question-scraper",
    thumbnail: "StackOverflowQuestionScraper.png",
    inProgress: false
  },
  {
    id: 4,
    name: "Ben's Exocortex",
    description: "A collection of resources, examples, and simple projects I'm making, to solidify some stuff I've learned and for practice.",
    techUsed: [],
    url: "",
    sourceUrl: "https://github.com/brombaut/BEC",
    thumbnail: "",
    inProgress: false,
    acronym: "BEC"
  },
  {
    id: 5,
    name: "Monkey Parser",
    description: "",
    techUsed: [
      "TypeScript",
      "Jest"
    ],
    url: "https://github.com/brombaut/monkey-ast-visualizer",
    sourceUrl: "https://github.com/brombaut/monkey-parser",
    thumbnail: "",
    inProgress: false,
    acronym: "AST"
  }
];

export default projects.sort(sortProjects);
