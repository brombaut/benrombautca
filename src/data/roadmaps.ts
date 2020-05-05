import { YearlyRoadmap } from "@/types/yearly-roadmap";

const roadmap2020: YearlyRoadmap = {
  year: 2020,
  tasks: [
    {
      description: "I want to learn the fundamentals of Machine Learning",
      actionItems: [
        {
          description: "I will complete the Stanford University Machine Learning online course.",
          done: false,
          footnote: ""
        },
        {
          description: "I will complete the Practical Analyses of Software Engineering Data lecture and lab series, which focuses on machine learning applications for software engineering.",
          done: false,
          footnote: ""
        },
        {
          description: "I will read the 'MIT Deep Learning Book'.",
          done: false,
          footnote: ""
        },
        {
          description: "I will implement a machine learning model that predicts whether an NHL team will win or lose a game.",
          done: false,
          footnote: ""
        }
      ]
    },
    {
      description: "I want to get more experience with network protocols",
      actionItems: [
        {
          description: "I will read 'Hands-On Network Programming with C'.",
          done: false,
          footnote: ""
        },
        {
          description: "I will build some sort of project related to networking (BitTorrent client, web client).",
          done: false,
          footnote: ""
        }
      ]
    },
    {
      description: "I want to learn more about Software Architecture and Design",
      actionItems: [
        {
          description: "I will read 'Clean Architecture'.",
          done: false,
          footnote: ""
        },
        {
          description: "I will read 'Design Patterns: Elements of Reusable Object-Oriented Software'.",
          done: false,
          footnote: ""
        },
        {
          description: "I will create UML diagrams for my projects.",
          done: false,
          footnote: ""
        }
      ]
    },
    {
      description: "I want to write more tests and learn TDD",
      actionItems: [
        {
          description: "I will complete problems from 'Cracking the Coding Interview' following TDD.",
          done: false,
          footnote: ""
        },
        {
          description: "I will use Jest with my frontend projects.",
          done: false,
          footnote: ""
        }
      ]
    },
    {
      description: "I want to learn TypeScript",
      actionItems: [
        {
          description: "I will build at least two projects with TypeScript.",
          done: true,
          footnote: ""
        }
      ]
    },
    {
      description: "I want to learn WebAssembly",
      actionItems: [
        {
          description: "I will build a manual floating-point conerver in C++, and build a frontend that uses it as a WASM module.",
          done: true,
          footnote: ""
        }
      ]
    }
  ]
};

const roadmaps: YearlyRoadmap[] = [
  roadmap2020
];

export default roadmaps;
