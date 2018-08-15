import "./polyfill";
import Vue from "vue";
import Buefy from "buefy";
import bugsnag from "./bugsnag";
import SearchBox from "./components/SearchBox";
import Changelog from "./components/Changelog";
import moment from "moment";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "header",
  components: {
    SearchBox,
    Changelog
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
        const clan = await (await fetch(
          `/clan/${newValue.replace("#", "")}/short.json`
        )).json();
        window.location = `/clan/${clan.slug}`;
      }
    }
  }
});

document
  .querySelectorAll("[data-from-now]")
  .forEach(i => (i.innerHTML = moment(i.dataset.fromNow).fromNow()));
