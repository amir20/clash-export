<template>
  <div ref="chart"></div>
</template>

<script>
import Chartist from "chartist";
import { bugsnagClient } from "../bugsnag";

export default {
  props: ["tag"],
  data() {
    return { data: null, chart: null };
  },
  async mounted() {
    try {
      this.data = await (await fetch(
        `/clan/${this.tag.replace("#", "")}/trophies.json`
      )).json();
    } catch (e) {
      console.error(e);
      bugsnagClient.notify(e);
    }

    this.chart = new Chartist.Line(
      this.$refs.chart,
      {
        labels: this.data.labels,
        series: [
          {
            name: "series-1",
            data: this.data.points
          }
        ]
      },
      {
        fullWidth: true,
        showArea: true,
        showPoint: false,
        showLine: false,
        width: "100%",
        height: "180px",
        axisX: { showGrid: false }
      }
    );
  }
};
</script>

<style scoped>

</style>
