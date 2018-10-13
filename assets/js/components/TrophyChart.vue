<template>
  <div ref="chart" class="trophy-chart"></div>
</template>

<script>
import * as d3 from "d3";
import { bugsnagClient } from "../bugsnag";

export default {
  props: ["tag"],
  data() {
    return { data: null, chart: null };
  },
  async created() {
    const json = await (await fetch(
      `/clan/${this.tag.replace("#", "")}/trophies.json`
    )).json();
    this.$nextTick(() => {
      const parseTime = d3.timeParse("%Y-%m-%d");
      const data = json.dates.map((key, i) => ({
        date: parseTime(key),
        trophies: json.trophies[i],
        members: json.members[i]
      }));
      this.data = data;

      const margin = { top: 10, right: 20, bottom: 10, left: 50 };
      const width = 960 - margin.left - margin.right;
      const height = 180 - margin.top - margin.bottom;

      const x = d3.scaleTime().range([0, width]);
      const yLeft = d3.scaleLinear().range([height, 0]);
      const yRight = d3.scaleLinear().range([height, 0]);

      const area = d3
        .area()
        .x(d => x(d.date))
        .y0(height)
        .y1(d => yLeft(d.trophies))
        .curve(d3.curveMonotoneX);

      const trophyLine = d3
        .line()
        .x(d => x(d.date))
        .y(d => yLeft(d.trophies))
        .curve(d3.curveMonotoneX);

      // define the line 1
      const membersLine = d3
        .line()
        .x(d => x(d.date))
        .y(d => yRight(d.members))
        .curve(d3.curveMonotoneX);

      const svg = d3
        .select(this.$refs.chart)
        .append("svg")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 960 200")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      x.domain(
        d3.extent(data, function(d) {
          return d.date;
        })
      );
      yLeft.domain(
        d3.extent(data, function(d) {
          return d.trophies;
        })
      );
      yRight.domain(
        d3.extent(data, function(d) {
          return d.members;
        })
      );

      svg
        .append("path")
        .data([data])
        .attr("class", "area")
        .attr("d", area);

      svg
        .append("path")
        .data([data])
        .attr("class", "line")
        .attr("d", trophyLine);

      svg
        .append("path")
        .data([data])
        .attr("class", "members-line")
        .attr("d", membersLine);

      // add the X Axis
      svg
        .append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(
          d3
            .axisBottom(x)
            .tickFormat(d3.timeFormat("%x"))
            .ticks(d3.timeDay.filter(d => d3.timeDay.count(0, d) % 4 === 0))
        );

      svg.append("g").call(d3.axisLeft(yLeft).ticks(4));

      svg
        .append("g")
        .attr("transform", "translate( " + width + ", 0 )")
        .call(d3.axisRight(yRight).ticks(4));
    });
  }
};
</script>

<style>
.trophy-chart {
  .line {
    fill: none;
    stroke: steelblue;
    stroke-width: 2px;
  }

  .members-line {
    fill: none;
    stroke: rgb(255, 19, 2);
    stroke-width: 1px;
  }

  .area {
    fill: lightsteelblue;
  }
}
</style>
