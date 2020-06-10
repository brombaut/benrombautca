import { YearlyRoadmap } from "@/roadmaps/yearly-roadmap";
import roadmap2019 from "./yearlyRoadmaps/roadmap2019";
import roadmap2020 from "./yearlyRoadmaps/roadmap2020";

const sortByYear = function (a: YearlyRoadmap, b: YearlyRoadmap) {
  if (a.year > b.year) return -1;
  return 1;
};

const roadmaps: YearlyRoadmap[] = [
  roadmap2019,
  roadmap2020
];

export default roadmaps.sort(sortByYear);
