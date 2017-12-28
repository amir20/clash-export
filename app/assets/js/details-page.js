import Vue from "vue";
import Buefy from "buefy";
import ClanTable from "./components/ClanTable";

Vue.use(Buefy);

new Vue({
  el: "#clan-table",
  components: {
    ClanTable
  }
});
