<template>
  <div class="container">
    <div ref="chart" class="activity-distribution has-loader" :class="{ 'is-loading': loading }"></div>
  </div>
</template>

<script>
import Chartist from "chartist";
import "chartist-plugin-legend";
import format from "date-fns/format";
import fill from "lodash/fill";
import times from "lodash/times";
import random from "lodash/random";
import { mapState } from "vuex";

export default {
  props: {
    name: { type: String }
  },
  data() {
    return { chart: null };
  },
  mounted() {
    this.draw(fakeData);
  },
  computed: {
    ...mapState(["loggedUserActivity", "playerActivity", "hasLoggedUser", "loading"]),
    data() {
      const dates = [];
      const thisUser = { name: "This player", data: [], className: "player-activity" };
      const loggedInUser = { name: "You", data: [], className: "logged-activity" };
      if (this.playerActivity[this.name]) {
        for (const [date, value] of Object.entries(this.playerActivity[this.name])) {
          dates.push(date);
          thisUser.data.push(value);
          if (this.loggedUserActivity[this.name] && this.loggedUserActivity[this.name][date]) {
            loggedInUser.data.push(this.loggedUserActivity[this.name][date]);
          } else if (this.hasLoggedUser) {
            loggedInUser.data.push(0);
          }
        }
      }
      return { dates, series: this.hasLoggedUser ? [thisUser, loggedInUser] : [thisUser] };
    }
  },
  watch: {
    data(newValue) {
      this.draw(newValue);
    }
  },
  methods: {
    redraw() {
      this.chart.update();
    },
    draw(data) {
      this.chart = new Chartist.Line(
        this.$refs.chart,
        {
          labels: data.dates,
          series: data.series
        },
        {
          plugins: [
            Chartist.plugins.legend({
              classNames: ["player-activity", "logged-activity"]
            })
          ],
          axisX: {
            showLabel: true,
            showGrid: false,
            labelInterpolationFnc: (value, index) => {
              if (index % 2 === 0) {
                return this.loading ? value : format(new Date(value), "MMM do");
              } else {
                return null;
              }
            }
          },
          axisY: {
            showLabel: true,
            showGrid: false,
            labelInterpolationFnc: value => value.toLocaleString()
          },
          width: "100%",
          fullWidth: true,
          showArea: true,
          showLine: true,
          showPoint: false,
          distributeSeries: true
        },
        [
          [
            "screen and (max-width: 860px)",
            {
              axisX: {
                labelInterpolationFnc: (value, index) => {
                  if (index % 10 === 0) {
                    return this.loading ? value : format(new Date(value), "MMM do");
                  } else {
                    return null;
                  }
                }
              }
            }
          ]
        ]
      );
    }
  }
};

const fakeData = {
  series: { data: [times(28, random.bind(0, 10))], name: "" },
  dates: fill(Array(28), "█")
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

  & /deep/ .logged-activity .ct-area {
    fill: none;
  }

  & /deep/ .logged-activity .ct-line {
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

      &.player-activity:before,
      &.ct-series-0:before {
        background-color: #00d1b2;
        border-color: #00d1b2;
        left: 6px;
      }

      &.logged-activity:before {
        background-color: hsl(348, 100%, 61%);
        border-color: hsl(348, 100%, 61%);
        left: 6px;
      }
    }
  }
}
</style>
