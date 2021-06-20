import Vue from "vue";
import VueRouter from "vue-router";
import AboutMeExtended from "@/aboutMe/AboutMeExtended.vue";
import BookshelfSection from "@/bookshelf/BookshelfSection.vue";
import ArticlesSection from "@/articles/ArticlesSection.vue";
import SoftwareSection from "@/software/SoftwareSection.vue";

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
    path: "/software",
    name: "software",
    component: SoftwareSection,
  },
];

const router = new VueRouter({
  mode: "hash",
  base: process.env.BASE_URL,
  routes,
});

export default router;
