import Vue from "vue";
import VueRouter from "vue-router";
import AboutMeExtended from "@/aboutMe/AboutMeExtended.vue";
import BookshelfSection from "@/bookshelf/BookshelfSection.vue";
import ArticlesSection from "@/articles/ArticlesSection.vue";
import SelectedArticleSection from "@/articles/SelectedArticleSection.vue";
import SoftwareSection from "@/software/SoftwareSection.vue";
import SelectedSoftwareSection from "@/software/SelectedSoftwareSection.vue";
import MarathonSection from "@/marathon/MarathonSection.vue";

Vue.use(VueRouter);

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
    path: "/marathon-22",
    name: "marathon-22",
    component: MarathonSection,
  },
];

const router = new VueRouter({
  mode: "hash",
  base: process.env.BASE_URL,
  routes,
});

export default router;
