<template>
  <div ref="chart"></div>
</template>

<script>
import dc from "dc";

import zip from "lodash/zip";
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
        const data = zip(this.data.labels, this.data.points).map(([d, p]) => ({
          key: d,
          value: p
        }));

        this.chart = dc.lineChart(this.$refs.chart);
        this.chart
          .width("100%")
          .height(480)
          .margins({ left: 50, top: 10, right: 10, bottom: 20 })
          .renderArea(true)
          .brushOn(false)
          .dimension({})
          .x({})
          .group({})
          .data(() => data)
          .render();
        // this.chart = new Chartist.Line(
        //   this.$refs.chart,
        //   {
        //     labels: this.data.labels,
        //     series: [
        //       {
        //         name: "series-1",
        //         data: this.data.points
        //       }
        //     ]
        //   },
        //   {
        //     fullWidth: true,
        //     showArea: true,
        //     showPoint: false,
        //     showLine: false,
        //     width: "100%",
        //     height: "180px",
        //     axisX: {
        //       showGrid: false,
        //       labelInterpolationFnc(value, index) {
        //         return index % 3 === 0
        //           ? new Date(value).toLocaleDateString()
        //           : null;
        //       }
        //     },
        //     axisY: {
        //       labelInterpolationFnc(value, index) {
        //         return value.toLocaleString();
        //       }
        //     }
        //   }
        // );
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
