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
  async created() {
    try {
      this.data = await (await fetch(
        `/clan/${this.tag.replace("#", "")}/trophies.json`
      )).json();
      this.$nextTick(() => {
        this.chart = new Chartist.Line(
          this.$refs.chart,
          {
            labels: this.data.dates,
            series: [
              {
                name: "series-1",
                data: this.data.trophies
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
            axisX: {
              showGrid: false,
              labelInterpolationFnc(value, index) {
                return index % 3 === 0
                  ? new Date(value).toLocaleDateString()
                  : null;
              }
            },
            axisY: {
              labelInterpolationFnc(value, index) {
                return value.toLocaleString();
              }
            }
          }
        );
      });
    } catch (e) {
      console.error(e);
      bugsnagClient.notify(e);
    }
  }
};
</script>

<style scoped>
</style>
