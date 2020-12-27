import Vue from "vue";
import { Dropdown, Autocomplete, Icon } from "buefy";
import bugsnag from "../bugsnag";
import SearchBox from "../components/SearchBox";
import Changelog from "../components/Changelog";
import User from "../components/User";
import { event } from "../ga";
import { apolloClient } from "../client";
import { gql } from "apollo-boost";

bugsnag(Vue);

Vue.use(Dropdown);
Vue.use(Autocomplete);
Vue.use(Icon);

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
        const { data } = await apolloClient.query({
          query: gql`
            query GetClan($tag: String!) {
              clan(tag: $tag) {
                slug
              }
            }
          `,
          variables: {
            tag: newValue
          }
        });
        window.location = `/clan/${data.clan.slug}`;
      }
    }
  }
});
