<template>
  <div class="columns">
    <div class="column">
      <div class="columns is-gapless is-vcentered">
        <b-field class="column is-narrow">
          <b-radio-button v-model="days" :native-value="1" type="is-danger">
            <b-icon icon="hourglass" size="is-small" pack="far"></b-icon>
            <span>Yesterday</span>
          </b-radio-button>
          <b-radio-button v-model="days" :native-value="7" type="is-success">
            <b-icon icon="calendar-alt" size="is-small" pack="far"></b-icon>
            <span>Last Week</span>
          </b-radio-button>
        </b-field>
        <b-field class="column is-hidden-mobile">
          <b-switch v-model="sort" true-value="delta" false-value="value"> Sort by difference </b-switch>
        </b-field>
      </div>
    </div>
    <div class="column is-narrow is-hidden-mobile">
      <download-button></download-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations } from "vuex";
import DownloadButton from "./DownloadButton";

export default {
  components: {
    DownloadButton,
  },
  data() {
    return {
      days: 7,
      sort: "value",
    };
  },
  methods: {
    ...mapActions({ loadDaysAgo: "SHOW_DIFFERENT_DAYS" }),
    ...mapMutations({ changeSort: "CHANGE_SORT_FIELD" }),
  },
  watch: {
    days(newValue) {
      if (newValue) {
        this.loadDaysAgo(newValue);
      }
    },
    sort(newValue) {
      if (newValue) {
        this.changeSort(newValue);
      }
    },
  },
};
</script>
<style lang="scss" scoped>
/deep/ .switch {
  margin-left: 2em;
}
</style>
