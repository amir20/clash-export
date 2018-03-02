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
        labels: [
          "Recent Gold Grab",
          "Recent Elixer Grab",
          "Recent DE Grab",
          "Recent Doations"
        ],
        series: [
          {
            name: this.playerData.name.value,
            data: this.playerSeries
          },
          {
            name: "Clan Average",
            data: this.avgSeries
          }
        ]
      },
      {
        seriesBarDistance: -20,
        horizontalBars: true,
        reverseData: true,
        width: "80%",
        height: "400px",
        plugins: [Chartist.plugins.legend()],
        axisY: {
          offset: 80
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
        this.playerData.totalGoldGrab.delta,
        this.playerData.totalElixirGrab.delta,
        this.playerData.totalDeGrab.delta,
        this.playerData.totalDonations.delta
      ];
    },
    avgSeries() {
      return [
        this.avg("totalGoldGrab"),
        this.avg("totalElixirGrab"),
        this.avg("totalDeGrab"),
        this.avg("totalDonations")
      ];
    }
  }
};
</script>

<style scoped>
.player-comparison>>>.ct-bar {
  stroke-width: 20px;
}
</style>
