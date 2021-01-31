<template>
  <div class="navbar-end">
    <changelog> </changelog>
    <div class="navbar-item nav-search-item">
      <div class="field is-expanded"><search-box :selected-tag.sync="selectedTag"></search-box></div>
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
};
</script>

<style></style>
