import "./polyfill";
import "@fortawesome/fontawesome-free/js/all";
import Vue from "vue";
import Buefy from "buefy";
import bugsnag from "./bugsnag";
import SearchBox from "./components/SearchBox";
import Changelog from "./components/Changelog";
import User from "./components/User";
import formatDistance from "date-fns/formatDistance";
import parse from "date-fns/parse";
import { event } from "./ga";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "header",
  components: {
    SearchBox,
    Changelog,
    User
  },
  data() {
    return {
      selectedTag: null,
      showNav: false
    };
  },
  watch: {
    async selectedTag(newValue) {
      if (newValue) {
        event("search-clans", "Search");
        const clan = await (await fetch(`/clan/${newValue.replace("#", "")}/short.json`)).json();
        window.location = `/clan/${clan.slug}`;
      }
    }
  }
});

const items = document.querySelectorAll("[data-from-now]");
[].forEach.call(
  items,
  i =>
    (i.innerHTML = formatDistance(parse(i.dataset.fromNow, "yyyy-MM-dd HH:mm:ss", new Date()), new Date(), {
      addSuffix: true
    }))
);
