<template>
  <div class="box" :class="{ 'still-loading': loading }">
    <article class="columns is-vcentered">
      <div class="column is-narrow has-text-centered-mobile">
        <img :src="clan.badgeUrls.medium" width="128" />
      </div>
      <div class="column">
        <div class="content">
          <div class="columns is-vcentered">
            <div class="column is-narrow">
              <h3 class="title is-3 is-marginless">
                {{ clan.name }}
              </h3>
            </div>
            <div class="column is-narrow mt-1">
              <div class="tags is-centered">
                <span class="tag is-light">
                  <i class="fas fa-hashtag mr-1"></i>
                  {{ clan.tag.substr(1) }}
                </span>
                <span class="tag is-light">
                  <i class="fas fa-user-friends mr-1"></i>
                  {{ clan.members }}
                </span>
              </div>
            </div>
          </div>

          <p class="content is-medium">{{ clan.description }}</p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
import { bugsnagClient } from "../bugsnag";
import { mapMutations } from "vuex";
import { request } from "../client";
import { gql } from "graphql-request";

export default {
  props: ["tag", "foundClan"],
  data() {
    return {
      loading: true,
      clan: {
        badgeUrls: {
          medium: "https://placehold.jp/250x250.png?text=%20",
        },
        name: "██████",
        tag: "██████",
        description: "██████ ████████████ █ ████ █ ██████ ████████████ ███ ███ ███████████ █ ███ ███",
        members: "█",
      },
    };
  },
  async created() {
    try {
      const { clan } = await request(
        gql`
          query GetClan($tag: String!) {
            clan(tag: $tag) {
              name
              members
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
        {
          tag: this.tag,
        }
      );
      this.clan = clan;
    } catch (e) {
      console.error(e);
      bugsnagClient.notify(e);
      this.$emit("error");
    }
    this.$emit("update:foundClan", this.clan);
    this.setFoundClan(this.clan);
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
