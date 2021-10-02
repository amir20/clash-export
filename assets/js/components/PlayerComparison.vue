<template>
  <div class="component">
    <div class="media" v-if="player">
      <figure class="media-left">
        <p class="image is-64x64" v-if="player.league"><img :src="player.league.iconUrls.medium" :alt="player.tag" /></p>
      </figure>
      <div class="media-content">
        <div class="content">
          <div class="level is-pulled-right is-marginless">
            <div class="level-item has-text-centered">
              <div>
                <div class="title is-size-4-mobile">{{ Math.ceil(this.playerData.activityScore.value) }} / 100</div>
                <div class="heading">Player Activity Score</div>
              </div>
            </div>
          </div>
          <h2 class="title is-marginless is-size-4-mobile">
            {{ player.name }} <small class="subtitle is-6">{{ player.role | role }}</small>
          </h2>
          <small class="subtitle is-5" v-if="player.league">{{ player.league.name }}</small>
        </div>
      </div>
    </div>
    <a class="button is-warning is-pulled-right" :href="`/player/${player.slug}`" v-if="player">
      <span class="icon"> <i class="fas fa-user"></i> </span> <span>View Player Profile</span>
    </a>
    <section>
      <h4 class="title is-4 is-marginless">Player Activity</h4>
      <player-activity :tag="playerData.tag.value"></player-activity>
    </section>
    <div class="is-touch-only">
      <a class="button is-info is-fullwidth-mobile" :href="`clashofclans://action=OpenPlayerProfile&amp;tag=${encodeURIComponent(this.playerData.tag.value)}`">
        <span class="icon"> <i class="fas fa-external-link-alt"></i></span> <span>Open Player in Game</span>
      </a>
    </div>
  </div>
</template>

<script>
import { bugsnagClient } from "../bugsnag";
import { request } from "../client";
import { gql } from "graphql-request";
import PlayerActivity from "./PlayerActivity.vue";

const role = {
  coLeader: "Co-leader",
  leader: "Leader",
  admin: "Elder",
  member: "Member",
};

export default {
  components: {
    PlayerActivity,
  },
  props: ["playerData"],
  data() {
    return {
      player: null,
    };
  },
  async created() {
    try {
      const data = await request(
        gql`
          query GetPlayerDetails($tag: String!) {
            player(tag: $tag) {
              name
              tag
              slug
              role
              league {
                name
                iconUrls {
                  medium
                }
              }
            }
          }
        `,
        {
          tag: this.playerData.tag.value,
        }
      );
      this.player = data.player;
    } catch (e) {
      console.error(e);
      bugsnagClient.notify(e);
    }
  },
  filters: {
    role(value) {
      return role[value];
    },
  },
  methods: {},
  watch: {},
  computed: {},
};
</script>

<style lang="scss" scoped>
@media screen and (max-width: 768px) {
  .is-fullwidth-mobile {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    width: 100%;
  }
}

.component {
  padding: 1em;
  width: calc(100vw - 1em);

  @media screen and (max-width: 769px) {
    & {
      padding: 1em 0;
    }
  }
}
</style>
