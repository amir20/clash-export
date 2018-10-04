<template>
  <div class="component">
    <div class="media" v-if="player">
      <figure class="media-left">
        <p class="image is-64x64" v-if="player.league">
          <img :src="player.league.iconUrls.small" :alt="player.tag">
        </p>
      </figure>
      <div class="media-content">
        <div class="content">
          <div class="level is-pulled-right">
            <div class="level-item has-text-centered">
              <div>
                <div class="title is-size-4-mobile">{{ Math.ceil(player.percentile * 100) }} / 100</div>
                <div class="heading">Player Activity Score</div>
              </div>
            </div>
          </div>
          <h2 class="title is-marginless is-size-4-mobile">{{ player.name }} <small class="subtitle is-6">{{ player.role | role }}</small></h2>
          <small class="subtitle is-5" v-if="player.league">{{ player.league.name }}</small>
        </div>
      </div>
    </div>
    <div>
      <div ref="chart" class="player-comparison"></div>
    </div>
    <div class="buttons is-right mobile is-hidden-desktop" v-if="player">
      <a class="button is-info is-fullwidth-mobile" :href="`clashofclans://action=OpenPlayerProfile&amp;tag=${encodeURIComponent(player.tag)}`">
        <span class="icon">
          <i class="fas fa-gamepad"></i>
        </span>
        <span>View Player in Game</span>
      </a>
    </div>
  </div>
</template>

<script>
import Chartist from "chartist";
import "chartist-plugin-legend";
import { bugsnagClient } from "../bugsnag";
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";

const role = {
  coLeader: "Co-leader",
  leader: "Leader",
  admin: "Elder",
  member: "Member"
};

export default {
  props: ["playerData"],
  data() {
    return {
      chart: null,
      player: null
    };
  },
  created() {
    this.fetchPlayer();
  },
  mounted() {
    this.chart = new Chartist.Bar(
      this.$refs.chart,
      {
        labels: ["Recent DE Grab", "Recent Elixer Grab", "Recent Gold Grab"],
        series: this.series
      },
      {
        seriesBarDistance: -20,
        horizontalBars: true,
        width: "100%",
        height: "400px",
        plugins: [Chartist.plugins.legend()],
        axisY: {},
        axisX: {
          labelInterpolationFnc(value, index) {
            return index % 2 === 0 ? value.toLocaleString() : null;
          }
        }
      }
    );
  },
  filters: {
    role(value) {
      return role[value];
    }
  },
  methods: {
    update() {
      this.chart.update({
        series: this.series
      });
    },
    async fetchPlayer() {
      try {
        this.player = await (await fetch(
          `/clan/${this.tag.replace(
            "#",
            ""
          )}/${this.playerData.tag.value.replace("#", "")}.json`
        )).json();
      } catch (e) {
        console.error(e);
        bugsnagClient.notify(e);
      }
    }
  },
  watch: {
    similarClansAvg(newValue) {
      if (newValue && newValue.gold_grab > 0) {
        this.update();
      }
    },
    clanStats(newValue) {
      if (newValue && newValue.gold_grab > 0) {
        this.update();
      }
    },
    savedClanStats(newValue) {
      if (newValue && newValue.gold_grab > 0) {
        this.update();
      }
    }
  },
  computed: {
    ...mapState(["similarClansAvg", "clanStats", "savedClanStats", "tag"]),
    series() {
      const s = [];
      s.push({
        name: this.playerData.name.value,
        data: [
          this.playerData.totalDeGrab.delta,
          this.playerData.totalElixirGrab.delta,
          this.playerData.totalGoldGrab.delta
        ],
        className: "player"
      });

      s.push({
        name: "This clan's average",
        data: [
          this.clanStats.de_grab,
          this.clanStats.elixir_grab,
          this.clanStats.gold_grab
        ],
        className: "clan"
      });

      s.push({
        name: "Similar clans' average",
        data: [
          this.similarClansAvg.de_grab,
          this.similarClansAvg.elixir_grab,
          this.similarClansAvg.gold_grab
        ],
        className: "similar-clans"
      });

      if (this.savedClanStats && this.savedClanStats.name) {
        s.push({
          name: this.savedClanStats.name,
          data: [
            this.savedClanStats.de_grab,
            this.savedClanStats.elixir_grab,
            this.savedClanStats.gold_grab
          ],
          className: "saved-clan"
        });
      }

      return s;
    }
  }
};
</script>

<style scoped>
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
