import "core-js/es/map";
import "core-js/es/set";
import "whatwg-fetch";
import "promise-polyfill/src/polyfill";
import Vue from "vue";
import Buefy from "buefy";
import bugsnag from "./bugsnag";
import SearchBox from "./components/SearchBox";
import Changelog from "./components/Changelog";
import User from "./components/User";
import formatDistance from "date-fns/formatDistance";
import parse from "date-fns/parse";
import { event } from "./ga";
import { apolloClient } from "./client";
import { gql } from "apollo-boost";

bugsnag(Vue);

Vue.use(Buefy, { defaultIconPack: "fa" });

new Vue({
  el: "#common-nav",
  components: {
    SearchBox,
    Changelog,
    User,
  },
  data() {
    return {
      selectedTag: null,
      showNav: false,
    };
  },
  watch: {
    async selectedTag(newValue) {
      if (newValue) {
        event("search-clans", "Search");
        const { data } = await apolloClient.query({
          query: gql`
            query GetClan($tag: String!) {
              clan(tag: $tag) {
                slug
              }
            }
          `,
          variables: {
            tag: newValue,
          },
        });
        window.location = `/clan/${data.clan.slug}`;
      }
    },
  },
});

const items = document.querySelectorAll("[data-from-now]");
[].forEach.call(
  items,
  (i) =>
    (i.innerHTML = formatDistance(parse(i.dataset.fromNow, "yyyy-MM-dd HH:mm:ss", new Date()), new Date(), {
      addSuffix: true,
    }))
);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/static/service-worker.js");
  });
}
