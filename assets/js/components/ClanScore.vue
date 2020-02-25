<template>
  <div class="columns is-vcentered is-mobile">
    <div class="column is-8 has-text-right">
      {{ title }}
    </div>
    <div class="column is-4 is-size-1">
      {{ score | grade }}
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

const grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E", "F"];

export default {
  props: {
    score: { type: Number },
    field: { type: String },
    title: { type: String }
  },
  data: function() {
    return {};
  },
  watch: {
    scoreValue(newValue, oldValue) {
      this.score = newValue;
    }
  },
  computed: {
    ...mapState(["clan"]),
    scoreValue() {
      return this.field.split(".").reduce((prev, curr) => (prev ? prev[curr] : null), this.clan);
    }
  },
  methods: {},
  filters: {
    grade(value) {
      const s = Math.ceil((100 - value * 100) / 3);
      return grades[Math.min(s, grades.length - 1)];
    }
  }
};
</script>
<style lang="scss">
.scoreboard .panel-block {
  display: block !important;
}
</style>
