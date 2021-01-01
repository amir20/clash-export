<template>
  <div class="container">
    <div ref="chart" class="activity-distribution has-loader" :class="{ 'is-loading': loading }"></div>
  </div>
</template>

<script>
import Chartist from "chartist";
import "chartist-plugin-legend";
import format from "date-fns/format";
import parse from "date-fns/parse";
import fill from "lodash/fill";
import times from "lodash/times";
import random from "lodash/random";

const dom = { chart: null };

export default {
  props: {
    labels: { type: Array },
    userSeries: { type: Array },
    playerSeries: { type: Array },
    showUser: { type: Boolean },
    loading: { type: Boolean, default: true },
  },
  mounted() {
    this.draw();
  },
  computed: {
    data() {
      const { labels, playerSeries, userSeries } = this;
      const player = { name: "This player", data: playerSeries, className: "player-activity" };
      const user = { name: "You", data: userSeries, className: "user-activity" };
      return { labels, series: this.showUser ? [player, user] : [player] };
    },
  },
  watch: {
    loading() {
      this.draw();
    },
  },
  methods: {
    redraw() {
      this.draw();
    },
    draw() {
      const data = this.loading ? fakeData : this.data;
      dom.chart = new Chartist.Line(
        this.$refs.chart,
        {
          labels: data.labels,
          series: data.series,
        },
        {
          plugins: [
            Chartist.plugins.legend({
              classNames: ["player-activity", "user-activity"],
            }),
          ],
          axisX: {
            showLabel: true,
            showGrid: false,
            labelInterpolationFnc: (value, index) => {
              if (index % 2 === 0) {
                return this.loading ? value : format(parse(value, "yyyy-MM-dd HH:mm:ss", new Date()), "MMM do");
              } else {
                return null;
              }
            },
          },
          axisY: {
            showLabel: true,
            showGrid: false,
            labelInterpolationFnc: (value) => value.toLocaleString(),
          },
          width: "100%",
          fullWidth: true,
          showArea: true,
          showLine: true,
          showPoint: false,
          distributeSeries: true,
        },
        [
          [
            "screen and (max-width: 860px)",
            {
              axisX: {
                labelInterpolationFnc: (value, index) => {
                  if (index % 10 === 0) {
                    return this.loading ? value : format(parse(value, "yyyy-MM-dd HH:mm:ss", new Date()), "MMM do");
                  } else {
                    return null;
                  }
                },
              },
            },
          ],
        ]
      );
    },
  },
};

const fakeData = {
  series: [{ data: times(28, random.bind(0, 10)), name: "This player" }],
  labels: fill(Array(28), "█"),
};
</script>

<style lang="scss" scoped>
.activity-distribution {
  width: 100%;
  margin-bottom: -41px;

  &.is-loading {
    opacity: 0.25;

    & /deep/ .ct-area {
      fill: #333;
    }
  }

  & /deep/ .player-activity .ct-area {
    fill: #00d1b2;
    fill-opacity: 0.85;
  }

  & /deep/ .player-activity .ct-line {
    stroke: none;
  }

  & /deep/ .user-activity .ct-area {
    fill: none;
  }

  & /deep/ .user-activity .ct-line {
    stroke: hsl(348, 100%, 61%);
    stroke-width: 2px;
    stroke-dasharray: 4, 2;
  }

  & /deep/ .ct-chart-line .ct-label {
    white-space: nowrap;
  }

  & /deep/ .ct-legend {
    font-size: 85%;
    position: absolute;
    right: 1em;

    li {
      display: inline;
      padding-right: 5px;
      white-space: nowrap;
      &:before {
        left: 6px;
      }

      &.player-activity:before,
      &.ct-series-0:before {
        background-color: #00d1b2;
        border-color: #00d1b2;
      }

      &.user-activity:before {
        background-color: hsl(348, 100%, 61%);
        border-color: hsl(348, 100%, 61%);
      }
    }
  }
}
</style>
