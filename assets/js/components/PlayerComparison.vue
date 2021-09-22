<template>
  <div class="component">
    <div class="media" v-if="player">
      <figure class="media-left">
        <p class="image is-64x64" v-if="player.league"><img :src="player.league.iconUrls.small" :alt="player.tag" /></p>
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
      <h4 class="title is-4 is-marginless">Loot Activity</h4>
      <div ref="chart" class="player-comparison"></div>
    </section>
    <div class="is-touch-only">
      <a class="button is-info is-fullwidth-mobile" :href="`clashofclans://action=OpenPlayerProfile&amp;tag=${encodeURIComponent(this.playerData.tag.value)}`">
        <span class="icon"> <i class="fas fa-external-link-alt"></i></span> <span>Open Player in Game</span>
      </a>
    </div>
  </div>
</template>

<script>
import Chartist from "chartist";
import "chartist-plugin-legend";
import { bugsnagClient } from "../bugsnag";
import Troops from "./Troops";
import { mapState } from "vuex";
import { request } from "../client";
import { gql } from "graphql-request";

const role = {
  coLeader: "Co-leader",
  leader: "Leader",
  admin: "Elder",
  member: "Member",
};

export default {
  components: {
    Troops,
  },
  props: ["playerData"],
  data() {
    return {
      player: null,
    };
  },
  created() {
    this.fetchPlayer();
  },
  mounted() {
    this.update();
  },
  filters: {
    role(value) {
      return role[value];
    },
  },
  methods: {
    update() {
      new Chartist.Bar(
        this.$refs.chart,
        {
          labels: ["Recent DE Grab", "Recent Elixir Grab", "Recent Gold Grab"],
          series: this.series,
        },
        {
          seriesBarDistance: -20,
          horizontalBars: true,
          width: "100%",
          height: "400px",
          plugins: [Chartist.plugins.legend()],
          axisX: {
            labelInterpolationFnc(value, index) {
              return index % 2 === 0 ? value.toLocaleString() : null;
            },
          },
        }
      );
    },
    async fetchPlayer() {
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
                    small
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
  },
  watch: {
    clan(newValue) {
      if (newValue && newValue.avgDeGrab > 0) {
        this.update();
      }
    },
    savedClan(newValue) {
      if (newValue && newValue.avgDeGrab > 0) {
        this.update();
      }
    },
    playerData(newValue) {
      if (newValue && newValue.name) {
        this.update();
      }
    },
  },
  computed: {
    ...mapState(["clan", "savedClan"]),
    series() {
      const s = [];
      s.push({
        name: this.playerData.name.value,
        data: [this.playerData.totalDeGrab.delta, this.playerData.totalElixirGrab.delta, this.playerData.totalGoldGrab.delta],
        className: "player",
      });

      s.push({
        name: "This clan's average",
        data: [this.clan.delta.avgDeGrab, this.clan.delta.avgElixirGrab, this.clan.delta.avgGoldGrab],
        className: "clan",
      });

      s.push({
        name: "Similar clans' average",
        data: [this.clan.similar.avgDeGrab, this.clan.similar.avgElixirGrab, this.clan.similar.avgGoldGrab],
        className: "similar-clans",
      });

      if (this.savedClan && this.savedClan.name) {
        s.push({
          name: this.savedClan.name,
          data: [this.savedClan.delta.avgDeGrab, this.savedClan.delta.avgElixirGrab, this.savedClan.delta.avgGoldGrab],
          className: "saved-clan",
        });
      }

      return s;
    },
  },
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

.player-comparison {
  position: relative;

  & /deep/ .ct-bar {
    stroke-width: 20px;
  }
  & /deep/ .player .ct-bar {
    stroke: hsl(141, 71%, 48%);
  }
  & /deep/ .clan .ct-bar {
    stroke: hsl(217, 71%, 53%);
  }
  & /deep/ .similar-clans .ct-bar {
    stroke: hsl(348, 100%, 61%);
  }

  & /deep/ .saved-clan .ct-bar {
    stroke: hsl(48, 100%, 67%);
  }

  & /deep/ .ct-legend {
    position: absolute;
    font-size: 90%;
    right: 20px;
    bottom: 50px;
    border: 1px solid #ccc;
    background: white;
    padding: 0.7em;
    border-radius: 3px;

    & .ct-series-0:before {
      background-color: hsl(141, 71%, 48%);
      border-color: hsl(141, 71%, 48%);
    }
    & .ct-series-1:before {
      background-color: hsl(217, 71%, 53%);
      border-color: hsl(217, 71%, 53%);
    }
    & .ct-series-2:before {
      background-color: hsl(348, 100%, 61%);
      border-color: hsl(348, 100%, 61%);
    }
    & .ct-series-3:before {
      background-color: hsl(48, 100%, 67%);
      border-color: hsl(48, 100%, 67%);
    }
  }
}
</style>
