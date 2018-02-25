import Vue from "vue";
import Buefy from "buefy";
import ClanTable from "./components/ClanTable";
import TableNav from "./components/TableNav";
import SearchBox from "./components/SearchBox";
import TrophyChart from "./components/TrophyChart";
import bugsnag from "./bugsnag";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

Vue.prototype.$bus = new Vue({});

new Vue({
  el: "#app",
  components: {
    ClanTable,
    TableNav,
    TrophyChart
  }
});

new Vue({
  el: ".navbar-start",
  components: {
    SearchBox
  },
  data() {
    return {
      selectedTag: null
    };
  },
  watch: {
    async selectedTag(newValue) {
      if (newValue) {
        const clan = await (await fetch(
          `/clan/${newValue.replace("#", "")}/short.json`
        )).json();
        window.location = `/clan/${clan.slug}`;
      }
    }
  }
});
