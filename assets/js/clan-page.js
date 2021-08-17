import Vue from "vue";
import Buefy from "buefy";
import VueRouter from "vue-router";

import bugsnag from "./bugsnag";
import store from "./store/clan-page";
import ClanPage from "./pages/ClanPage";
import ClanCWL from "./pages/ClanCWL";
import ClanPlayers from "./pages/ClanPlayers";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });
Vue.use(VueRouter);

const routes = [
  { path: "/cwl", component: ClanCWL, name: "cwl" },
  { path: "/", component: ClanPlayers, name: "players" },
];

const router = new VueRouter({
  routes,
  mode: "history",
  base: new URL(document.querySelector('link[rel="canonical"]').href).pathname,
});

new Vue({
  router,
  store,
  components: {
    ClanPage,
  },
  render: (h) => h(ClanPage),
}).$mount("#app");

store.dispatch("FETCH_CLAN_DATA");
