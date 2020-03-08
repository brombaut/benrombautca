import Vue from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUserSecret, faHome, faStreetView } from '@fortawesome/free-solid-svg-icons';
import { faFolderOpen, faEnvelope, faMap } from '@fortawesome/free-regular-svg-icons';
import { faGithub, faLinkedin } from '@fortawesome/free-brands-svg-icons';


import App from './App.vue';

library.add(faUserSecret);
library.add(faHome);
library.add(faFolderOpen);
library.add(faEnvelope);
library.add(faStreetView);
library.add(faMap);
library.add(faGithub);
library.add(faLinkedin);

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

new Vue({
    render: (h) => h(App),
}).$mount('#app');
