<template>
  <div class="container">
    <div ref="chart" class="attacks-distribution has-loader" :class="{ 'is-loading': loading }"></div>
  </div>
</template>

<script>
import Chartist from "chartist";
import format from "date-fns/format";
import debounce from "lodash/debounce";
import fill from "lodash/fill";
import times from "lodash/times";
import random from "lodash/random";

import { mapGetters, mapActions, mapMutations, mapState } from "vuex";

export default {
  props: ["playerTag"],
  data() {
    return { data: null, chart: null, started: false, loading: false };
  },
  async created() {
    this.loading = true;
    this.data = await (await fetch(`/player/${this.playerTag.replace("#", "")}/attacks.json`)).json();
    this.loading = false;
    this.$nextTick(() => {
      this.draw(this.data);
    });
  },
  mounted() {
    this.draw(fakeData);
  },
  methods: {
    animationStarted: debounce(function() {
      this.started = true;
    }, 1000),
    draw(data) {
      new Chartist.Line(
        this.$refs.chart,
        {
          labels: data.dates,
          series: [data.attackWins]
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
          showLine: false,
          showPoint: false,
          distributeSeries: true
        }
      );
    }
  }
};

const fakeData = {
  attackWins: times(28, random.bind(0, 10)),
  dates: fill(Array(28), "███ █")
};
</script>

<style scoped>
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

  & /deep/ .ct-area {
    fill: #00d1b2;
    fill-opacity: 0.85;
  }
}
</style>
