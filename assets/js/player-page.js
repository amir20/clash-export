import Vue from "vue";
import Buefy from "buefy";
import Troops from "./components/Troops";
import AttacksDistribution from "./components/AttacksDistribution";
import bugsnag from "./bugsnag";
bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#app",
  components: {
    Troops,
    AttacksDistribution
  }
});
