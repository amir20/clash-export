import Vue from "vue";
import Buefy from "buefy";
import ClanTable from "./components/ClanTable";
import Tabs from "./components/Tabs";
import bugsnag from "./bugsnag"

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });


Vue.prototype.$bus = new Vue({})

new Vue({
  el: "#clan-table",
  components: {
    ClanTable
  }
});

new Vue({
  el: "#tabs",
  components: {
    Tabs
  }
});
