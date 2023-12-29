<template>
  <div ref="chart" class="trophy-chart"></div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import { select } from "d3-selection";
import { extent } from "d3-array";
import { timeFormat, timeParse } from "d3-time-format";
import { scaleLinear, scaleTime } from "d3-scale";
import { area, curveMonotoneX, line } from "d3-shape";
import { axisBottom, axisLeft, axisRight } from "d3-axis";
import { timeDay } from "d3-time";
import debounce from "lodash/debounce";
import zip from "lodash/zip";

const d3 = {
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
  timeDay,
  area,
  curveMonotoneX,
};

const parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S+00:00Z");

const margin = { top: 10, right: 50, bottom: 40, left: 70 };
const height = 190 - margin.top - margin.bottom;
const dom = {
  svg: null,
  trophyPath: null,
  membersPath: null,
  bottomAxis: null,
  leftAxis: null,
  rightAxis: null,
  rightLabel: null,
  leftLabel: null,
};
export default {
  props: [],
  data() {
    return {
      data: [],
    };
  },
  computed: {
    ...mapState(["clan"]),
  },
  watch: {
    "clan.trophyHistory": function (newVal, oldVal) {
      this.refresh();
    },
  },
  created() {
    this.refresh();
  },
  mounted() {
    dom.svg = d3
      .select(this.$refs.chart)
      .append("svg")
      .attr("width", "100%")
      .attr("height", height + margin.top + margin.bottom);

    const root = dom.svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    dom.trophyPath = root.append("path").attr("class", "area");
    dom.membersPath = root.append("path").attr("class", "members-line");
    dom.bottomAxis = root.append("g").attr("class", "axis x");
    dom.leftAxis = root.append("g").attr("class", "axis y");
    dom.rightAxis = root.append("g").attr("class", "axis y");
    dom.rightLabel = root.append("text").attr("transform", "rotate(90)").attr("dy", "1em").style("text-anchor", "middle").attr("y", 1000).attr("x", 1000);

    dom.rightLabel.append("tspan").attr("class", "members-legend").text("◼ ");
    dom.rightLabel.append("tspan").text("Members");

    dom.leftLabel = root.append("text").attr("transform", "rotate(-90)").attr("dy", "1em").style("text-anchor", "middle").attr("y", 1000).attr("x", 1000);
    dom.leftLabel.append("tspan").attr("class", "trophy-legend").text("◼ ");
    dom.leftLabel.append("tspan").text("Trophy Points");

    window.addEventListener("resize", this.render);
  },
  destroyed() {
    window.removeEventListener("resize", this.render);
  },
  methods: {
    refresh() {
      this.data = [];
      const { labels, clanPoints, members } = this.clan.trophyHistory;
      for (const [date, trophy, member] of zip(labels, clanPoints, members)) {
        this.data.push({
          date: parseTime(date),
          trophies: trophy,
          members: member,
        });
      }
      this.$nextTick(this.render);
    },
    render: debounce(function () {
      const { svg, membersPath, trophyPath, bottomAxis, leftAxis, rightAxis, rightLabel, leftLabel } = dom;
      const { data } = this;

      const width = svg.node().getBoundingClientRect().width - margin.left - margin.right;
      const x = d3.scaleTime().range([0, width]);
      const yLeft = d3.scaleLinear().range([height, 0]);
      const yRight = d3.scaleLinear().range([height, 0]);

      const trophyArea = d3
        .area()
        .x((d) => x(d.date))
        .y0(height)
        .y1((d) => yLeft(d.trophies))
        .curve(d3.curveMonotoneX);

      const membersLine = d3
        .line()
        .x((d) => x(d.date))
        .y((d) => yRight(d.members))
        .curve(d3.curveMonotoneX);

      x.domain(d3.extent(data, (d) => d.date));
      yLeft.domain(d3.extent(data, (d) => d.trophies));
      const [yRightMin, yRightMax] = d3.extent(data, (d) => d.members);
      yRight.domain([Math.min(yRightMax - 5, yRightMin), yRightMax]);

      trophyPath.data([data]).attr("d", trophyArea);
      membersPath.data([data]).attr("d", membersLine);

      bottomAxis.attr("transform", "translate(0," + height + ")").call(
        d3
          .axisBottom(x)
          .tickFormat(d3.timeFormat("%b %-d"))
          .ticks(d3.timeDay.every(width > 1000 ? 2 : 3)),
      );

      leftAxis.call(d3.axisLeft(yLeft).ticks(4, "s"));

      rightAxis.attr("transform", "translate( " + width + ", 0 )").call(d3.axisRight(yRight).ticks(4));

      rightLabel.attr("y", 0 - width - margin.right).attr("x", height / 2);
      leftLabel.attr("y", 0 - margin.left).attr("x", -height / 2);
    }, 10),
  },
};
</script>

<style lang="scss" scoped>
.trophy-chart {
  margin-top: 3.5em;

  ::v-deep .members-line {
    fill: none;
    stroke: hsl(204, 86%, 53%);
    stroke-width: 1px;
    stroke-dasharray: 4, 2;
  }

  ::v-deep .trophy-legend {
    fill: #d70206;
    fill-opacity: 0.4;
  }

  ::v-deep .members-legend {
    fill: hsl(204, 86%, 53%);
  }

  ::v-deep .area {
    fill: #d70206;
    fill-opacity: 0.4;
  }

  ::v-deep text {
    fill: rgba(0, 0, 0, 0.6);
    font-family: "Titillium Web";
    font-size: 13px;
  }

  ::v-deep .axis.x .domain {
    stroke: rgba(0, 0, 0, 0.25);
  }

  ::v-deep .axis.y .domain {
    stroke: none;
  }

  ::v-deep .axis line {
    stroke: none;
  }
}
</style>
