<template>
  <div class="navbar-end">
    <changelog> </changelog>
    <div class="navbar-item nav-search-item">
      <div class="field is-expanded"><search-box :selected-clan.sync="selectedClan"></search-box></div>
    </div>
    <user> </user>
  </div>
</template>

<script>
import SearchBox from "./SearchBox";
import Changelog from "./Changelog";
import User from "./User";
import { event } from "../ga";
import { request } from "../client";
import { gql } from "graphql-request";

export default {
  components: {
    SearchBox,
    Changelog,
    User,
  },
  data() {
    return {
      selectedClan: null,
      showNav: false,
    };
  },
  watch: {
    async selectedClan() {
      if (this.selectedClan) {
        event("search-clans", "Search");
        if (this.selectedClan.slug == null) {
          const { clan } = await request(
            gql`
              query GetClan($tag: String!) {
                clan(tag: $tag) {
                  slug
                }
              }
            `,
            {
              tag: this.selectedClan.tag,
            }
          );
          window.location = `/clan/${clan.slug}`;
        } else {
          window.location = `/clan/${this.selectedClan.slug}`;
        }
      }
    },
  },
};
</script>

<style></style>
