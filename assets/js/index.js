import Vue from "vue";
import Buefy from "buefy";
import Home from "./components/Home";
import bugsnag from "./bugsnag";
import store from "./store/index-page";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#home",
  store,
  components: {
    Home,
  },
  render: (h) => h(Home),
});
