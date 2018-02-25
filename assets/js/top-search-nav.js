import Vue from "vue";
import Buefy from "buefy";
import SearchBox from "./components/SearchBox";

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: ".navbar-start",
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
