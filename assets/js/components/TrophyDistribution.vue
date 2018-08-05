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
          showLabel: true,
          showGrid: true
        },
        width: "100%",
        fullWidth: true,
        distributeSeries: true
      }
    );

    this.chart.on("draw", function(data) {
      if (data.type == "bar") {
        data.element.animate({
          y2: {
            dur: "400ms",
            from: data.y1,
            to: data.y2,
            easing: Chartist.Svg.Easing.easeOutQuint
          }
        });
      }
    });
    this.chart.on("created", function() {
      chart.detach(); // it will detach resize and media query listeners
    });
  }
};
</script>

<style scoped>
.trophy-distribution {
  width: 960px;
  margin: 0 auto;

  & /deep/ .ct-bar {
    stroke-width: 6px;
    stroke: #bbb;
    stroke-linecap: round;
  }
}
</style>
