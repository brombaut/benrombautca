import { YearlyRoadmap } from "@/types/yearly-roadmap";

const roadmap2020: YearlyRoadmap = {
  year: 2020,
  tasks: [
    {
      description: "I want to learn the fundamentals of Machine Learning",
      actionItems: [
        {
          description: "I will complete the Stanford University Machine Learning online course.",
          done: true,
          footnote: ""
        },
        {
          description: "I will complete the Practical Analyses of Software Engineering Data lecture and lab series, which focuses on machine learning applications for software engineering.",
          done: false,
          footnote: ""
        },
        {
          description: "I will read the \"MIT Deep Learning Book\".",
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
          description: "I will read \"Hands-On Network Programming with C\".",
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
          description: "I will read \"Clean Architecture: A Craftsman's Guide to Software Structure and Design\".",
          done: true,
          footnote: ""
        },
        {
          description: "I will read \"Design Patterns: Elements of Reusable Object-Oriented Software\".",
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
          description: "I will complete problems from \"Cracking the Coding Interview\" following TDD.",
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
          description: "I will build a manual floating-point converter in C++, and build a front-end that uses it as a WASM module.",
          done: false,
          footnote: ""
        }
      ]
    },
    {
      description: "Books I want to read",
      actionItems: [
        {
          description: "\"The Clean Coder: A Code of Conduct for Professional Programmers\"",
          done: true,
          footnote: ""
        },
        {
          description: "\"The Mythical Man-Month: Essays on Software Engineering\"",
          done: true,
          footnote: ""
        },
        {
          description: "\"The Phoenix Project: A Novel about IT, DevOps, and Helping Your Business Win\"",
          done: false,
          footnote: ""
        },
        {
          description: "\"The Annotated Turing: A Guided Tour Through Alan Turing's Historic Paper on Computability and the Turing Machine\"",
          done: false,
          footnote: ""
        },
        {
          description: "\"97 Things Every Programmer Should Know: Collective Wisdom from the Experts\"",
          done: true,
          footnote: ""
        },
        {
          description: "\"How Linux Works: What Every Superuser Should Know\"",
          done: false,
          footnote: ""
        }
      ]
    }
  ]
};

export default roadmap2020;
