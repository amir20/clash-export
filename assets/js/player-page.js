import Vue from "vue";
import Buefy from "buefy";
import Troops from "./components/Troops";
import PlayerActivityWrapper from "./components/PlayerActivityWrapper";
import PlayerRecommendation from "./components/PlayerRecommendation";
import bugsnag from "./bugsnag";
import store from "./store/player-page";
bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#troops",
  store,
  components: {
    Troops,
  },
  render: (h) => h(Troops),
});

// new Vue({
//   el: "#recommendation",
//   store,
//   components: {
//     PlayerRecommendation,
//   },
//   render: (h) => h(PlayerRecommendation),
// });

new Vue({
  el: "#activity",
  store,
  components: {
    PlayerActivityWrapper,
  },
  render: (h) => h(PlayerActivityWrapper),
});
