import { createApp } from "vue";
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
  faChevronLeft,
  faChevronRight,
  faMapMarkerAlt,
  faCalendar,
  faBuilding,
  faUniversity,
  faMapMarkedAlt,
  faCheck,
  faCircle,
  faEllipsisH,
  faBookOpen,
  faStar,
  faBars,
  faSchool,
  faPenSquare,
  faVial,
  faPortrait,
  faAddressCard,
  faRunning,
  faUsers,
  faParagraph,
  faHiking,
} from "@fortawesome/free-solid-svg-icons";
import { faEnvelope, faMap } from "@fortawesome/free-regular-svg-icons";
import { faGithub, faLinkedin, faDev, faStackOverflow, faResearchgate, faGoogleScholar } from "@fortawesome/free-brands-svg-icons";
import router from "./site-header/router";

import App from "./App.vue";

library.add(faUser);
library.add(faUsers);
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
library.add(faChevronLeft);
library.add(faChevronRight);
library.add(faMapMarkerAlt);
library.add(faCalendar);
library.add(faBuilding);
library.add(faUniversity);
library.add(faMapMarkedAlt);
library.add(faCheck);
library.add(faCircle);
library.add(faEllipsisH);
library.add(faBookOpen);
library.add(faStar);
library.add(faBars);
library.add(faSchool);
library.add(faDev);
library.add(faStackOverflow);
library.add(faPenSquare);
library.add(faVial);
library.add(faPortrait);
library.add(faAddressCard);
library.add(faRunning);
library.add(faResearchgate);
library.add(faParagraph);
library.add(faGoogleScholar);
library.add(faHiking);

const app = createApp({
  render: (h: any) => h(App),
});
app.use(router);
app.component("font-awesome-icon", FontAwesomeIcon);
app.mount("#app");
