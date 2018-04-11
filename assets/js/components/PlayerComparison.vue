<template>
  <div>
    <p class="title">{{ playerData.name.value }}</p>
    <div ref="chart" class="player-comparison"></div>
  </div>
</template>

<script>
import Chartist from "chartist";
import "chartist-plugin-legend";
import { bugsnagClient } from "../bugsnag";
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";

export default {
  props: ["playerData"],
  data() {
    return { chart: null };
  },
  mounted() {
    this.chart = new Chartist.Bar(
      this.$refs.chart,
      {
        labels: ["Recent DE Grab", "Recent Elixer Grab", "Recent Gold Grab"],
        series: [
          {
            name: this.playerData.name.value,
            data: this.playerSeries,
            className: "player"
          },
          {
            name: "This clan's average",
            data: this.clanAverage,
            className: "clan"
          },
          {
            name: "Similar clans' average",
            data: [
              this.similarClansAvg.de_grab,
              this.similarClansAvg.elixir_grab,
              this.similarClansAvg.gold_grab
            ],
            className: "similar-clans"
          }
        ]
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
  methods: {
    update() {
      this.chart.update({
        series: [
          {
            name: this.playerData.name.value,
            data: this.playerSeries,
            className: "player"
          },
          {
            name: "This clan's average",
            data: this.clanAverage,
            className: "clan"
          },
          {
            name: "Similar clans' average",
            data: [
              this.similarClansAvg.de_grab,
              this.similarClansAvg.elixir_grab,
              this.similarClansAvg.gold_grab
            ],
            className: "similar-clans"
          }
        ]
      });
    }
  },
  watch: {
    similarClansAvg(newValue) {
      if (newValue && newValue.gold_grab > 0) {
        this.update();
      }
    },
    clanAverage(newValue) {
      if (newValue && newValue[0] > 0) {
        this.update();
      }
    }
  },
  computed: {
    ...mapGetters(["clanAverage"]),
    ...mapState(["similarClansAvg"]),
    playerSeries() {
      return [
        this.playerData.totalDeGrab.delta,
        this.playerData.totalElixirGrab.delta,
        this.playerData.totalGoldGrab.delta
      ];
    }
  }
};
</script>

<style scoped>
.player-comparison {
  position: relative;
  width: calc(100vw - 4em);

  & >>> .ct-bar {
    stroke-width: 20px;
  }
  & >>> .player .ct-bar {
    stroke: hsl(141, 71%, 48%);
  }
  & >>> .clan .ct-bar {
    stroke: hsl(217, 71%, 53%);
  }
  & >>> .similar-clans .ct-bar {
    stroke: hsl(348, 100%, 61%);
  }
  & >>> .ct-legend {
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
  }
}
</style>
