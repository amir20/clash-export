<template>
  <div class="columns is-vcentered is-mobile">
    <div class="column has-text-right">
      {{ title }}
    </div>
    <div class="column is-size-1 has-text-weight-light" :class="gradeColor(score)">
      {{ score | grade }}
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

const grades = ["Max", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E", "E", "E", "F"];

export default {
  props: {
    field: { type: String },
    title: { type: String },
  },
  computed: {
    ...mapState(["clan"]),
    score() {
      return this.field.split(".").reduce((prev, curr) => (prev ? prev[curr] : null), this.clan);
    },
  },
  methods: {
    gradeColor(value) {
      const grade = this.$options.filters.grade(value);
      const classes = [];

      if (["M"].indexOf(grade.charAt(0)) > -1) {
        classes.push("has-text-success");
      }

      if (["A"].indexOf(grade.charAt(0)) > -1) {
        classes.push("has-text-success");
      }

      if (["B", "C"].indexOf(grade.charAt(0)) > -1) {
        classes.push("has-text-grey");
      }

      if (["D", "E", "F"].indexOf(grade.charAt(0)) > -1) {
        classes.push("has-text-danger");
      }

      return classes;
    },
  },
  filters: {
    grade(value) {
      const s = Math.ceil((100 - value * 100) / 3);
      return grades[Math.min(s, grades.length - 1)];
    },
  },
};
</script>
<style lang="scss">
.scorecard .panel-block {
  display: block !important;
}
</style>

<style lang="scss" scoped></style>
