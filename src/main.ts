import Vue from "vue";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faUser,
  faCode,
  faFolderOpen,
  faExternalLinkAlt,
  faGraduationCap,
  faBriefcase,
  faCaretDown,
  faMapMarkerAlt,
  faCalendar,
  faBuilding,
  faUniversity
} from "@fortawesome/free-solid-svg-icons";
import { faEnvelope, faMap } from "@fortawesome/free-regular-svg-icons";
import { faGithub, faLinkedin } from "@fortawesome/free-brands-svg-icons";


import App from "./App.vue";

library.add(faUser);
library.add(faFolderOpen);
library.add(faEnvelope);
library.add(faMap);
library.add(faGithub);
library.add(faLinkedin);
library.add(faCode);
library.add(faExternalLinkAlt);
library.add(faGraduationCap);
library.add(faBriefcase);
library.add(faCaretDown);
library.add(faMapMarkerAlt);
library.add(faCalendar);
library.add(faBuilding);
library.add(faUniversity);

// eslint-disable-next-line import/prefer-default-export
export const bus = new Vue();

Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.config.productionTip = false;

new Vue({
  render: (h) => h(App)
}).$mount("#app");
