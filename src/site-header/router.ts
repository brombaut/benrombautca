import { createWebHashHistory, createRouter } from "vue-router";
import AboutMeExtended from "@/aboutMe/AboutMeExtended.vue";
import BookshelfSection from "@/bookshelf/BookshelfSection.vue";
import ArticlesSection from "@/articles/ArticlesSection.vue";
import SelectedArticleSection from "@/articles/SelectedArticleSection.vue";
import SoftwareSection from "@/software/SoftwareSection.vue";
import SelectedSoftwareSection from "@/software/SelectedSoftwareSection.vue";
import PublicationsSection from "@/publications/PublicationsSection.vue";
import RunningSection from "@/running/RunningSection.vue";
import HikingSection from "@/hiking/HikingSection.vue";

const routes = [
  {
    path: "/",
    name: "land",
    component: AboutMeExtended,
  },
  {
    path: "/about-me",
    name: "aboutMe",
    component: AboutMeExtended,
  },
  {
    path: "/work",
    name: "work",
    component: AboutMeExtended,
  },
  {
    path: "/education",
    name: "education",
    component: AboutMeExtended,
  },
  {
    path: "/bookshelf",
    name: "bookshelf",
    component: BookshelfSection,
  },
  {
    path: "/articles",
    name: "articles",
    component: ArticlesSection,
  },
  {
    path: "/articles/:articleId",
    name: "selectedArticle",
    component: SelectedArticleSection,
  },
  {
    path: "/software",
    name: "software",
    component: SoftwareSection,
  },
  {
    path: "/software/:softwareId",
    name: "selectedSoftware",
    component: SelectedSoftwareSection,
  },
  {
    path: "/publications",
    name: "publications",
    component: PublicationsSection,
  },
  {
    path: "/running",
    name: "running",
    component: RunningSection,
  },
  {
    path: "/hiking",
    name: "hiking",
    component: HikingSection,
  },
];

// TODO: Maybe change this to html5 - https://router.vuejs.org/guide/essentials/history-mode.html
const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
