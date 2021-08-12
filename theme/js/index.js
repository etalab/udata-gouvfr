import { createApp } from "vue";

import Threads from "./components/discussions/threads.vue";
import Suggest from "./components/search/suggest-box";
import Search from "./components/search/search";
import FollowButton from "./components/utils/follow-button";

import Tabs from "./components/vanilla/tabs";
import Accordion from "./components/vanilla/accordion";
import Clipboard from "./components/vanilla/clipboard";

import VueFinalModal from "vue-final-modal";
import Toaster from "@meforma/vue-toaster";

import Api from "./plugins/api";
import Auth from "./plugins/auth";
import Modals from "./plugins/modals";
import i18n from "./plugins/i18n";
import bodyClass from "./plugins/bodyClass";
import filters from "./plugins/filters";

import InitSentry from "./sentry";

const app = createApp({});

// Configure as early as possible in the app's lifecycle
InitSentry(app);

app.use(Api);
app.use(Auth);
app.use(VueFinalModal());
app.use(Modals); //Has to be loaded after VueFinalModal
app.use(i18n);
app.use(bodyClass);
app.use(filters);
app.use(Toaster);

app.component("discussion-threads", Threads);
app.component("suggest", Suggest);
app.component("search", Search);
app.component("follow-button", FollowButton);

//We keep the div HTML from before trying to mount the VueJS App
const previousHtml = document.querySelector("#app").innerHTML;

try {
  app.mount("#app");
} catch (e) {
  //If the mount wasn't successful, Vue will remove all HTML from the div. We'll put it back so you can use the website.
  document.querySelector("#app").innerHTML = previousHtml;

  console.log(
    "VueJS template compilation failed. Aborted the process and rolled back the HTML. See error(s) above and below (probably won't help you tho) :"
  );
  console.error(e);
  throw e;
}

console.log("JS is injected !");
