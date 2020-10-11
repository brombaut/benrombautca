import { Work } from "./work";

const workEntities: Work[] = [
  {
    title: "Teaching Assistant",
    company: "Queen's University",
    time: "Sep '20 - Present",
    location: "Kingston, Ontario",
    workedWith: [],
    imageFile: "queensName.png",
    link: "https://www.queensu.ca/",
  },
  {
    title: "Software Developer",
    company: "Eigen Innovations",
    time: "May '19 - Apr '20",
    location: "Fredericton, New Brunswick",
    workedWith: ["C/C++", "Django", "Vue", "PSQL", "Electron"],
    imageFile: "eigenLogo_Large.png",
    link: "https://eigen.io/",
  },
  {
    title: "Front-End Developer (Co-op)",
    company: "Eigen Innovations",
    time: "Apr '18 - Aug '18",
    location: "Fredericton, New Brunswick",
    workedWith: ["Vue", "Web Development", "Product Design"],
    imageFile: "eigenLogo_Large.png",
    link: "https://eigen.io/",
  },
  {
    title: "Undergraduate Research Assistant (Co-op)",
    company: "Human-Computer Interaction Lab - UNB",
    time: "May '17 - Aug '17",
    location: "Fredericton, New Brunswick",
    workedWith: ["Java", "Android Development", "Bluetooth LE"],
    imageFile: "hcilabLogo_Large.png",
    link: "https://hcilab.github.io/",
  },
  {
    title: "Quality Assurance Analyst (Co-op)",
    company: "Siemens Canada",
    time: "Sep '16 - Dec '16",
    location: "Fredericton, New Brunswick",
    workedWith: ["Java", "JavaScript", "QA Practices"],
    imageFile: "siemensLogo_Large.png",
    link: "https://new.siemens.com/ca/en.html",
  },
  {
    title: "Software Developer (Co-op)",
    company: "Brunswick News Inc.",
    time: "Jan '16 - Apr '16",
    location: "Fredericton, New Brunswick",
    workedWith: ["Web Development", "jQuery", "C#"],
    imageFile: "brunswickNewsLogo_Large.png",
    link: "https://www.linkedin.com/company/brunswick-news-inc-/?originalSubdomain=ca",
  },
  {
    title: "IT Support Specialist (Co-op)",
    company: "Brunswick News Inc.",
    time: "May '15 - Aug '15",
    location: "Saint John, New Brunswick",
    workedWith: ["Customer/IT Support"],
    imageFile: "brunswickNewsLogo_Large.png",
    link: "https://www.linkedin.com/company/brunswick-news-inc-/?originalSubdomain=ca",
  },
];

export default workEntities;
