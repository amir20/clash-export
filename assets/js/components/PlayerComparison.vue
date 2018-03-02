<template>
  <div ref="chart" class="player-comparison"></div>
</template>

<script>
import Chartist from "chartist";
import "chartist-plugin-legend";
import { bugsnagClient } from "../bugsnag";

export default {
  props: ["playerData", "allData"],
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
            name: "Clan Average",
            data: this.avgSeries,
            className: "clan"
          }
        ]
      },
      {
        seriesBarDistance: -20,
        horizontalBars: true,
        width: "80%",
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
    avg(column) {
      return (
        this.allData.reduce(
          (total, player) => total + player[column].delta,
          0
        ) / this.allData.length
      );
    }
  },
  computed: {
    playerSeries() {
      return [
        this.playerData.totalDeGrab.delta,
        this.playerData.totalElixirGrab.delta,
        this.playerData.totalGoldGrab.delta
      ];
    },
    avgSeries() {
      return [
        this.avg("totalDeGrab"),
        this.avg("totalElixirGrab"),
        this.avg("totalGoldGrab")
      ];
    }
  }
};
</script>

<style scoped>
.player-comparison {
  &>>>.ct-bar {
    stroke-width: 20px;
  }
  &>>>.player .ct-bar {
    stroke: hsl(141, 71%, 48%);
  }
  &>>>.clan .ct-bar {
    stroke: hsl(217, 71%, 53%);
  }
  &>>>.ct-legend .ct-series-0:before {
    background-color: hsl(141, 71%, 48%);
    border-color: hsl(141, 71%, 48%);
  }
  &>>>.ct-legend .ct-series-1:before {
    background-color: hsl(217, 71%, 53%);
    border-color: hsl(217, 71%, 53%);
  }
}
</style>
