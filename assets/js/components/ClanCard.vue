<template>
  <div class="box" :class="{ 'still-loading': loading }">
    <article class="columns is-vcentered">
      <div class="column is-narrow has-text-centered-mobile">
        <img :src="this.data.badgeUrls.medium" width="64" />
      </div>
      <div class="column">
        <div class="content">
          <p>
            <strong>{{ this.data.name }}</strong>
            <small>
              <i class="fa fa-tag fa-lg" aria-hidden="true"></i> {{ this.data.tag }} <i class="fa fa-trophy fa-lg" aria-hidden="true"></i>
              {{ this.data.clanPoints.toLocaleString() }}
            </small>
            <br />
            {{ this.data.description }}
          </p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
import { bugsnagClient } from "../bugsnag";
import { mapMutations } from "vuex";
import { apolloClient } from "../client";
import { gql } from "@apollo/client/core";

export default {
  props: ["tag", "foundClan"],
  data() {
    return {
      loading: true,
      data: {
        badgeUrls: {
          medium: "https://placehold.jp/250x250.png?text=%20",
        },
        name: "██████",
        tag: "██████",
        description: "██████ ████████████ █ ████ █ ██████ ████████████ ███ ███ ███████████ █ ███ ███",
        clanPoints: "0",
      },
    };
  },
  async created() {
    try {
      const { data } = await apolloClient.query({
        query: gql`
          query GetClan($tag: String!) {
            clan(tag: $tag) {
              name
              clanPoints
              tag
              slug
              description
              players {
                name
                tag
                trophies
              }
              badgeUrls {
                medium
              }
            }
          }
        `,
        variables: {
          tag: this.tag,
        },
      });
      this.data = data.clan;
    } catch (e) {
      console.error(e);
      bugsnagClient.notify(e);
      this.$emit("error");
    }
    this.$emit("update:foundClan", this.data);
    this.setFoundClan(this.data);
    this.loading = false;
  },
  methods: {
    ...mapMutations(["setFoundClan"]),
  },
};
</script>
<style lang="scss" scoped>
.still-loading * {
  color: #efefef !important;
}
</style>
