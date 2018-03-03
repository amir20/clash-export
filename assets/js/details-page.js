import Vue from "vue";
import Buefy from "buefy";
import ClanTable from "./components/ClanTable";
import TableNav from "./components/TableNav";
import TrophyChart from "./components/TrophyChart";
import bugsnag from "./bugsnag";
import "./top-search-nav";
import store from './store'
bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

Vue.prototype.$bus = new Vue({});

new Vue({
  el: "#app",
  store,
  components: {
    ClanTable,
    TableNav,
    TrophyChart
  }
});
