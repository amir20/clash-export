import Vue from "vue";
import Buefy from "buefy";
import ClanTable from "./components/ClanTable";
import ClanPageHeader from "./components/ClanPageHeader";
import TableNav from "./components/TableNav";
import bugsnag from "./bugsnag";
import store from "./store/clan-page";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#clan-page-header",
  store,
  components: {
    ClanPageHeader,
  },
  render: (h) => h(ClanPageHeader),
});

new Vue({
  el: "#table-nav",
  store,
  components: {
    TableNav,
  },
  render: (h) => h(TableNav),
});

new Vue({
  el: "#clan-table",
  store,
  components: {
    ClanTable,
  },
  render: (h) => h(ClanTable),
});

store.dispatch("FETCH_CLAN_DATA");
