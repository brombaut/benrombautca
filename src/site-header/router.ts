import { createWebHashHistory, createRouter } from "vue-router";

const routes = [
  {
    path: "/",
    name: "land",
    component: () => import("@/aboutMe/AboutMeExtended.vue"),
  },
  {
    path: "/about-me",
    name: "aboutMe",
    component: () => import("@/aboutMe/AboutMeExtended.vue"),
  },
  {
    path: "/work",
    name: "work",
    component: () => import("@/aboutMe/AboutMeExtended.vue"),
  },
  {
    path: "/education",
    name: "education",
    component: () => import("@/aboutMe/AboutMeExtended.vue"),
  },
  {
    path: "/bookshelf",
    name: "bookshelf",
    component: () => import("@/bookshelf/BookshelfSection.vue"),
  },
  {
    path: "/articles",
    name: "articles",
    component: () => import("@/articles/ArticlesSection.vue"),
  },
  {
    path: "/articles/:articleId",
    name: "selectedArticle",
    component: () => import("@/articles/SelectedArticleSection.vue"),
  },
  {
    path: "/software",
    name: "software",
    component: () => import("@/software/SoftwareSection.vue"),
  },
  {
    path: "/software/:softwareId",
    name: "selectedSoftware",
    component: () => import("@/software/SelectedSoftwareSection.vue"),
  },
  {
    path: "/publications",
    name: "publications",
    component: () => import("@/publications/PublicationsSection.vue"),
  },
  {
    path: "/running",
    name: "running",
    component: () => import("@/running/RunningSection.vue"),
  },
  {
    path: "/hiking",
    name: "hiking",
    component: () => import("@/hiking/HikingSection.vue"),
  },
];

// TODO: Maybe change this to html5 - https://router.vuejs.org/guide/essentials/history-mode.html
const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
