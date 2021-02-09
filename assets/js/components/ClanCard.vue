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
            <div class="column mt-1">
              <div class="field is-grouped is-grouped-multiline">
                <div class="control">
                  <div class="tags has-addons are-small">
                    <span class="tag is-dark"><i class="fas fa-hashtag"></i></span>
                    <span class="tag is-light">{{ clan.tag.substr(1) }}</span>
                  </div>
                </div>
                <div class="control">
                  <div class="tags has-addons are-small">
                    <span class="tag is-dark"><i class="fas fa-user-friends"></i></span>
                    <span class="tag is-light">{{ clan.members }}</span>
                  </div>
                </div>
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

<style lang="scss">
.tags.are-small .tag:not(.is-normal):not(.is-large):not(.is-medium) {
  font-size: 0.65rem;
}
</style>
