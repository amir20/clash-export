import Vue from "vue";
import Buefy from "buefy";
import Troops from "./components/Troops";
import PlayerActivity from "./components/PlayerActivity";
import PlayerRecommendation from "./components/PlayerRecommendation";
import bugsnag from "./bugsnag";
import store from "./store/player-page";
bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#app",
  store,
  components: {
    Troops,
    PlayerRecommendation,
    PlayerActivity,
  },
});
