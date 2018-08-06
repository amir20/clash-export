import Vue from "vue";
import Buefy from "buefy";
import ClanTable from "./components/ClanTable";
import TableNav from "./components/TableNav";
import TrophyChart from "./components/TrophyChart";
import Notification from "./components/Notification";
import LastUpdated from "./components/LastUpdated";
import bugsnag from "./bugsnag";
import store from "./store/details-page";
bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#app",
  store,
  components: {
    ClanTable,
    TableNav,
    TrophyChart,
    Notification,
    LastUpdated
  }
});
