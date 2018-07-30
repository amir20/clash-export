<template>
  <div ref="chart" class="trophy-distribution"></div>
</template>

<script>
import Chartist from "chartist";
import { bugsnagClient } from "../bugsnag";

export default {
  data() {
    return { data: null, chart: null };
  },
  created() {
    this.data = window.__DISTRIBUTION__;
  },
  mounted() {
    this.chart = new Chartist.Bar(
      this.$refs.chart,
      {
        labels: this.data.labels,
        series: this.data.values
      },
      {
        axisX: {
          showLabel: false,
          showGrid: false
        },
        axisY: {
          showLabel: false,
          showGrid: false
        },
        width: "100%",
        fullWidth: true,
        distributeSeries: true
      }
    );
  }
};
</script>

<style scoped>
.trophy-distribution {
  & /deep/ .ct-bar {
    stroke-width: 6px;
    stroke: #ff3860 !important;
    stroke-linecap: round;
  }
}
</style>
