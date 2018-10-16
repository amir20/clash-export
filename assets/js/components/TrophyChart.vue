<template>
  <div ref="chart" class="trophy-chart"></div>
</template>

<script>
import { select } from "d3-selection";
import { extent } from "d3-array";
import { timeFormat } from "d3-time-format";
import { scaleLinear, scaleTime } from "d3-scale";
import { line, area } from "d3-shape";

import { bugsnagClient } from "../bugsnag";

// https://www.giacomodebidda.com/how-to-import-d3-plugins-with-webpack/
const d3 = Object.assign(
  {},
  {
    select,
    extent,
    timeFormat,
    range,
    scaleLinear,
    scaleTime,
    line,
    area
  }
);

export default {
  props: ["tag"],
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

      const margin = { top: 10, right: 30, bottom: 10, left: 50 };
      const width = 960 - margin.left - margin.right;
      const height = 140 - margin.top - margin.bottom;

      const x = d3.scaleTime().range([0, width]);
      const yLeft = d3.scaleLinear().range([height, 0]);
      const yRight = d3.scaleLinear().range([height, 0]);

      const trophyArea = d3
        .area()
        .x(d => x(d.date))
        .y0(height)
        .y1(d => yLeft(d.trophies))
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
        .attr("viewBox", "0 0 960 150")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      x.domain(d3.extent(data, d => d.date));
      yLeft.domain(d3.extent(data, d => d.trophies));
      const [yRightMin, yRightMax] = d3.extent(data, d => d.members);
      yRight.domain([Math.min(yRightMax - 5, yRightMin), yRightMax]);

      svg
        .append("path")
        .data([data])
        .attr("class", "area")
        .attr("d", trophyArea);

      svg
        .append("path")
        .data([data])
        .attr("class", "members-line")
        .attr("d", membersLine);

      // add the X Axis
      svg
        .append("g")
        .attr("transform", "translate(0," + height + ")")
        .attr("class", "axis x")
        .call(
          d3
            .axisBottom(x)
            .tickFormat(d3.timeFormat("%x"))
            .ticks(10)
        );

      svg
        .append("g")
        .attr("class", "axis y")
        .call(d3.axisLeft(yLeft).ticks(4));

      svg
        .append("g")
        .attr("transform", "translate( " + width + ", 0 )")
        .attr("class", "axis y")
        .call(d3.axisRight(yRight).ticks(4));
    });
  }
};
</script>

<style scoped>
.trophy-chart {
  /deep/ .members-line {
    fill: none;
    stroke: hsl(204, 86%, 53%);
    stroke-width: 1px;
    stroke-dasharray: 4, 2;
  }

  /deep/ .area {
    fill: #d70206;
    fill-opacity: 0.4;
  }

  /deep/ .axis text {
    color: rgba(0, 0, 0, 0.6);
    font-family: "Titillium Web";
  }

  /deep/ .axis.x .domain {
    stroke: rgba(0, 0, 0, 0.25);
  }
  /deep/ .axis.y .domain {
    stroke: none;
  }

  /deep/ .axis line {
    stroke: none;
  }
}
</style>
