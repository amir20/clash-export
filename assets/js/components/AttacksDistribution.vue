<template>
  <div class="container">
    <div ref="chart" class="attacks-distribution has-loader" :class="{ 'is-loading': loading }"></div>
  </div>
</template>

<script>
import Chartist from "chartist";
import format from "date-fns/format";
import fill from "lodash/fill";
import times from "lodash/times";
import random from "lodash/random";
import UserMixin from "../user";

export default {
  props: ["playerTag"],
  mixins: [UserMixin],
  data() {
    return { savedPlayerData: {}, data: null, chart: null, loading: false, compareUser: false };
  },
  async created() {
    this.loading = true;

    if (this.hasUser && this.playerTag !== this.userTag) {
      this.compareUser = true;
      this.savedPlayerData = await (await fetch(`/player/${this.userTag.replace("#", "")}/attacks.json`)).json();
    }
    const json = await (await fetch(`/player/${this.playerTag.replace("#", "")}/attacks.json`)).json();
    const dates = [];
    const attackWins = [];
    const playerWins = [];
    for (const [date, attacks] of Object.entries(json)) {
      dates.push(date);
      attackWins.push(attacks);
      if (this.savedPlayerData[date]) {
        playerWins.push(this.savedPlayerData[date]);
      } else {
        playerWins.push(0);
      }
    }
    this.data = { dates, series: this.compareUser ? [attackWins, playerWins] : [attackWins] };
    this.loading = false;
    this.$nextTick(() => {
      this.draw(this.data);
    });
  },
  mounted() {
    this.draw(fakeData);
  },
  methods: {
    draw(data) {
      new Chartist.Line(
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
.attacks-distribution {
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
}
</style>
