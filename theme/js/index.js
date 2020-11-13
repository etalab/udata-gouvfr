import Vue from "vue/dist/vue.js";

import Tabs from "./components/tabs.js";
import Accordion from "./components/accordion";

import Clipboard from "v-clipboard";
import VModal from "vue-js-modal";

import { showModal } from "./components/vue/modals";

Vue.use(Clipboard);
Vue.use(VModal);

new Vue({
  el: "#app",
  delimiters: ["[[", "]]"],
  methods: {
    showModal
  },
});

console.log("JS is injected !");