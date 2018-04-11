import Vue from "vue";
import Buefy from "buefy";
import ClanTable from "./components/ClanTable";
import TableNav from "./components/TableNav";
import TrophyChart from "./components/TrophyChart";
import Notification from "./components/Notification";
import bugsnag from "./bugsnag";
import store from "./store";
bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#app",
  store,
  components: {
    ClanTable,
    TableNav,
    TrophyChart,
    Notification
  }
});

let ticking = false;
const items = [
  document.querySelector(".hero.is-warning.is-bold"),
  document.querySelector("nav.navbar"),
  document.querySelector("footer")
];

items.forEach(item => (item.style.position = "relative"));
window.addEventListener("scroll", function(e) {
  const leftOffset = window.scrollX;

  if (!ticking) {
    window.requestAnimationFrame(function() {
      items.forEach(item => (item.style.left = leftOffset + "px"));
      ticking = false;
    });
    ticking = true;
  }
});
