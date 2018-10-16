<template>
  <div ref="chart" class="trophy-chart"></div>
</template>

<script>
import { select } from "d3-selection";
import { extent } from "d3-array";
import { timeFormat, timeParse } from "d3-time-format";
import { scaleLinear, scaleTime } from "d3-scale";
import { line, area, curveMonotoneX } from "d3-shape";
import { axisBottom, axisLeft, axisRight } from "d3-axis";
import debounce from "lodash/debounce";

// https://www.giacomodebidda.com/how-to-import-d3-plugins-with-webpack/
const d3 = Object.assign(
  {},
  {
    axisBottom,
    axisLeft,
    axisRight,
    select,
    extent,
    timeFormat,
    timeParse,
    scaleLinear,
    scaleTime,
    line,
    area,
    curveMonotoneX
  }
);

const margin = { top: 10, right: 30, bottom: 40, left: 50 };
const height = 190 - margin.top - margin.bottom;

export default {
  props: ["tag"],
  data() {
    return {
      data: [],
      svg: null,
      root: null,
      trophyPath: null,
      membersPath: null,
      bottomAxis: null,
      leftAxis: null,
      rightAxis: null,
      clientWidth: window.innerWidth
    };
  },
  async created() {
    const json = await (await fetch(
      `/clan/${this.tag.replace("#", "")}/trophies.json`
    )).json();
    const parseTime = d3.timeParse("%Y-%m-%d");
    this.data = json.dates.map((key, i) => ({
      date: parseTime(key),
      trophies: json.trophies[i],
      members: json.members[i]
    }));
    this.$nextTick(this.render);
  },
  mounted() {
    this.svg = d3.select(this.$refs.chart).append("svg");
    const root = this.svg
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    this.trophyPath = root.append("path").attr("class", "area");
    this.membersPath = root.append("path").attr("class", "members-line");
    this.bottomAxis = root.append("g").attr("class", "axis x");
    this.leftAxis = root.append("g").attr("class", "axis y");
    this.rightAxis = root.append("g").attr("class", "axis y");

    window.addEventListener("resize", this.render);
  },
  destroyed() {
    window.removeEventListener("resize", this.render);
  },
  methods: {
    render: debounce(function() {
      const {
        data,
        svg,
        membersPath,
        trophyPath,
        bottomAxis,
        leftAxis,
        rightAxis
      } = this;

      let width = this.$refs.chart.clientWidth - margin.left - margin.right;
      if (window.innerWidth < this.clientWidth) {
        width -= this.clientWidth - window.innerWidth;
      }

      this.clientWidth = window.innerWidth;

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

      svg
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

      x.domain(d3.extent(data, d => d.date));
      yLeft.domain(d3.extent(data, d => d.trophies));
      const [yRightMin, yRightMax] = d3.extent(data, d => d.members);
      yRight.domain([Math.min(yRightMax - 5, yRightMin), yRightMax]);

      trophyPath.data([data]).attr("d", trophyArea);
      membersPath.data([data]).attr("d", membersLine);

      bottomAxis.attr("transform", "translate(0," + height + ")").call(
        d3
          .axisBottom(x)
          .tickFormat(d3.timeFormat("%x"))
          .ticks(width > 1000 ? 9 : 6)
      );

      leftAxis.call(d3.axisLeft(yLeft).ticks(4));

      rightAxis
        .attr("transform", "translate( " + width + ", 0 )")
        .call(d3.axisRight(yRight).ticks(4));
    }, 150)
  }
};
</script>

<style scoped>
.trophy-chart {
  margin-top: 3.5em;
  overflow: hidden;

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
    font-size: 1.2em;
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
