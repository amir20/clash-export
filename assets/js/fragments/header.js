import Vue from "vue";
import { Dropdown, Autocomplete, Icon } from "buefy";
import bugsnag from "../bugsnag";
import SearchBox from "../components/SearchBox";
import Changelog from "../components/Changelog";
import User from "../components/User";
import { event } from "../ga";
import { request } from "../client";
import { gql } from "graphql-request";

bugsnag(Vue);

Vue.use(Dropdown);
Vue.use(Autocomplete);
Vue.use(Icon);

new Vue({
  el: "header",
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
        const data = await request(
          gql`
            query GetClan($tag: String!) {
              clan(tag: $tag) {
                slug
              }
            }
          `,
          {
            tag: newValue,
          }
        );
        window.location = `/clan/${data.clan.slug}`;
      }
    },
  },
});
