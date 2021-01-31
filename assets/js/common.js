import Vue from "vue";
import { Dropdown, Autocomplete, Icon } from "buefy";
import bugsnag from "./bugsnag";
import formatDistance from "date-fns/formatDistance";
import parse from "date-fns/parse";
import NavBarEnd from "./components/NavBarEnd";

bugsnag(Vue);

Vue.use(Dropdown);
Vue.use(Autocomplete);
Vue.use(Icon);

new Vue({
  el: "#nav-end",
  components: {
    NavBarEnd,
  },
  render: (h) => h(NavBarEnd),
});

const items = document.querySelectorAll("[data-from-now]");
[].forEach.call(
  items,
  (i) =>
    (i.innerHTML = formatDistance(parse(i.dataset.fromNow, "yyyy-MM-dd HH:mm:ss", new Date()), new Date(), {
      addSuffix: true,
    }))
);

document.querySelector(".navbar-burger.burger").addEventListener("click", (e) => {
  e.target.classList.toggle("is-active");
  document.querySelector(".navbar .navbar-menu").classList.toggle("is-active");
});
