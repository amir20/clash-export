import "whatwg-fetch";
import "promise-polyfill/src/polyfill";
import Vue from "vue";
import Buefy from "buefy";
import bugsnag from "./bugsnag";
import SearchBox from "./components/SearchBox";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "header",
  components: {
    SearchBox
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
