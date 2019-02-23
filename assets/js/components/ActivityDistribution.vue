<template>
  <div class="container">
    <div ref="chart" class="activity-distribution has-loader" :class="{ 'is-loading': loading }"></div>
  </div>
</template>

<script>
import Chartist from "chartist";
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
      const thisUser = [];
      const loggedInUser = [];
      if (this.playerActivity[this.name]) {
        for (const [date, value] of Object.entries(this.playerActivity[this.name])) {
          dates.push(date);
          thisUser.push(value);
          if (this.loggedUserActivity[this.name] && this.loggedUserActivity[this.name][date]) {
            loggedInUser.push(this.loggedUserActivity[this.name][date]);
          } else if (this.hasLoggedUser) {
            loggedInUser.push(0);
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
            showGrid: false
          },
          width: "100%",
          fullWidth: true,
          showArea: true,
          showLine: true,
          showPoint: false,
          distributeSeries: true
        }
      );
    }
  }
};

const fakeData = {
  series: [times(28, random.bind(0, 10))],
  dates: fill(Array(28), "█")
};
</script>

<style lang="scss" scoped>
.activity-distribution {
  width: 100%;
  margin-bottom: -41px;
  min-width: 960px;

  &.is-loading {
    opacity: 0.25;

    & /deep/ .ct-area {
      fill: #333;
    }
  }

  & /deep/ .ct-series-a .ct-area {
    fill: #00d1b2;
    fill-opacity: 0.85;
  }

  & /deep/ .ct-series-a .ct-line {
    stroke: none;
  }

  & /deep/ .ct-series-b .ct-area {
    fill: none;
  }

  & /deep/ .ct-series-b .ct-line {
    stroke: hsl(348, 100%, 61%);
    stroke-width: 2px;
    stroke-dasharray: 4, 2;
  }

  & /deep/ .ct-chart-line .ct-label {
    white-space: nowrap;
  }
}
</style>
