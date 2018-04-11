import Vue from "vue";
import Buefy from "buefy";
import bugsnag from "./bugsnag";
import SearchBox from "./components/SearchBox";
import browser from "./util/brower"

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: ".navbar",
  components: {
    SearchBox
  },
  data() {
    return {
      selectedTag: null
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

document.documentElement.classList.add(browser);
