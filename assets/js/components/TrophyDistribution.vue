<template>
  <div ref="chart" class="trophy-distribution"></div>
</template>

<script>
import Chartist from "chartist";
import debounce from "lodash/debounce";
import { mapState } from "vuex";

export default {
  data() {
    return { data: null, chart: null, started: false };
  },
  created() {
    this.data = window.__DISTRIBUTION__;
  },
  mounted() {
    const { labels } = this.data;
    const chart = new Chartist.Bar(
      this.$refs.chart,
      {
        labels: this.data.labels,
        series: this.data.values,
      },
      {
        axisX: {
          showLabel: true,
          showGrid: false,
          labelInterpolationFnc(value, index) {
            return index % 20 === 0 ? value.toLocaleString() : null;
          },
        },
        axisY: {
          showLabel: true,
          showGrid: true,
        },
        width: "100%",
        fullWidth: true,
        distributeSeries: true,
      }
    );

    chart.on("created", () => {
      this.highlightClan(this.foundClan);
    });

    chart.on("draw", (data) => {
      if (data.type === "bar") {
        this.animationStarted();
        if (!this.started) {
          data.element.animate({
            y2: {
              dur: "350ms",
              from: data.y1,
              to: data.y2,
              easing: Chartist.Svg.Easing.easeOutQuint,
            },
          });
        }
        data.element.attr({ label: labels[data.seriesIndex] });
      }
    });

    this.chart = chart;
  },
  methods: {
    animationStarted: debounce(function () {
      this.started = true;
    }, 1000),
    highlightClan(clan) {
      const oldBar = this.$refs.chart.querySelector("line.ct-bar.highlight");
      if (oldBar) {
        oldBar.classList.remove("highlight");
      }
      if (clan) {
        const label = clan.clanPoints - (clan.clanPoints % 500);
        const bar = this.$refs.chart.querySelector(`line[label='${label}'].ct-bar`);
        if (bar) {
          bar.classList.add("highlight");
        }
      }
    },
  },
  watch: {
    foundClan(newValue) {
      this.highlightClan(newValue);
    },
  },
  computed: {
    ...mapState(["foundClan"]),
  },
};
</script>

<style lang="scss" scoped>
.trophy-distribution {
  width: 960px;
  margin: 0 auto;

  & /deep/ .ct-bar {
    stroke-width: 6px;
    stroke: #bbb;

    &.highlight {
      stroke: #ff3860;
    }
  }
}
</style>
