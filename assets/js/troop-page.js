import Vue from "vue";
import bugsnag from "./bugsnag";
import TroopAverageDistribution from "./components/TroopAverageDistribution";

bugsnag(Vue);

new Vue({
  el: "#app",
  components: {
    TroopAverageDistribution,
  },
});
