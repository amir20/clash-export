<template>
  <div ref="chart" class="troops-average"></div>
</template>

<script>
import Chartist from "chartist";

export default {
  props: ["averages"],
  mounted() {
    new Chartist.Bar(
      this.$refs.chart,
      {
        labels: this.data.levels,
        series: this.data.series,
      },
      {
        axisX: {
          showLabel: true,
          showGrid: false,
        },
        axisY: {
          showLabel: true,
          showGrid: true,
        },
        width: "100%",
        height: "300px",
        stackBars: true,
      }
    );
  },
  computed: {
    data() {
      const levels = [];
      const averages = [];
      const deltas = [];
      const data = this.averages.sort(({ level: a }, { level: b }) => a - b);
      for (const { level, max, avg } of data) {
        levels.push(level);
        averages.push(+avg);
        deltas.push(+max - +avg);
      }
      return { levels, series: [averages, deltas] };
    },
  },
};
</script>

<style lang="scss" scoped>
.troops-average {
  & /deep/ .ct-bar {
    stroke-width: 50px;
  }

  & /deep/ .ct-series-a .ct-bar {
    stroke: hsl(348, 100%, 61%);
  }
  & /deep/ .ct-series-b .ct-bar {
    stroke: hsl(0, 0%, 85%);
  }
}
</style>
