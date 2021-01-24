import Vue from "vue";
import Buefy from "buefy";
import ClanTable from "./components/ClanTable";
import DownloadButton from "./components/DownloadButton";
import TableNav from "./components/TableNav";
import TrophyChart from "./components/TrophyChart";
import Notification from "./components/Notification";
import LastUpdated from "./components/LastUpdated";
import ClanField from "./components/ClanField";
import ClanScore from "./components/ClanScore";
import bugsnag from "./bugsnag";
import store from "./store/clan-page";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#app",
  store,
  components: {
    ClanTable,
    DownloadButton,
    TableNav,
    TrophyChart,
    Notification,
    LastUpdated,
    ClanField,
    ClanScore,
  },
});

store.dispatch("FETCH_CLAN_DATA");
