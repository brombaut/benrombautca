import Vue from "vue";
import VueRouter from "vue-router";
import LandingSection from "@/landing/LandingSection.vue";
import AboutMeSection from "@/aboutMe/AboutMeSection.vue";
import AboutMeExtended from "@/aboutMe/AboutMeExtended.vue";
import ProjectsSection from "@/projects/ProjectsSection.vue";
import WorkEducationSection from "@/workEducation/WorkEducationSection.vue";
import RoadMapsSection from "@/roadmaps/RoadMapsSection.vue";
import BookshelfSection from "@/bookshelf/BookshelfSection.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "landing",
    component: LandingSection,
  },
  {
    path: "/about-me",
    name: "aboutMe",
    component: AboutMeExtended,
  },
  {
    path: "/work-education",
    name: "workEducation",
    component: WorkEducationSection,
  },
  {
    path: "/projects",
    name: "projects",
    component: ProjectsSection,
  },
  {
    path: "/bookshelf",
    name: "bookshelf",
    component: BookshelfSection,
  },
  {
    path: "/roadmaps",
    name: "roadmaps",
    component: RoadMapsSection,
  },
];

const router = new VueRouter({
  mode: "hash",
  base: process.env.BASE_URL,
  routes,
});

export default router;
