<template>
  <div>
    <b-field>
      <b-radio-button v-model="days" :native-value="1" type="is-danger">
        <b-icon icon="hourglass" size="is-small" pack="far"></b-icon>
        <span>Yesterday</span>
      </b-radio-button>
      <b-radio-button v-model="days" :native-value="7" type="is-success">
        <b-icon icon="calendar-alt" size="is-small" pack="far"></b-icon>
        <span>Last Week</span>
      </b-radio-button>
    </b-field>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      days: 7,
      sort: "value"
    };
  },
  methods: {
    ...mapActions({ loadDaysAgo: "SHOW_DIFFERENT_DAYS" })
  },
  watch: {
    days(newValue) {
      if (newValue) {
        this.loadDaysAgo(newValue);
      }
    }
  }
};
</script>
