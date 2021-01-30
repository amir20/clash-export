import Vue from "vue";
import Buefy from "buefy";
import Home from "./components/Home";
import TrophyDistribution from "./components/TrophyDistribution";
import bugsnag from "./bugsnag";
import store from "./store/index-page";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#home",
  store,
  components: {
    Home,
    TrophyDistribution,
  },
  render: (h) => h(Home),
});

new Vue({
  el: "#distribution",
  store,
  components: {
    TrophyDistribution,
  },
  render: (h) => h(TrophyDistribution),
});
