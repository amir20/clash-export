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
      <b-dropdown multiple v-model="selectedGroups" aria-role="list" :triggers="['hover']">
        <template #trigger>
          <b-button type="is-primary" icon-right="fa fa-angle-down" icon-left="fas fa-columns"> Columns </b-button>
        </template>

        <b-dropdown-item v-for="group in allGroups" :key="group" :value="group" aria-role="listitem">
          <div class="media">
            <div class="media-left"></div>
            <div class="media-content">
              <h3 class="is-capitalized">{{ group }}</h3>
            </div>
          </div>
        </b-dropdown-item>
      </b-dropdown>
      <download-button></download-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
import DownloadButton from "./DownloadButton";

export default {
  components: {
    DownloadButton,
  },
  data() {
    return {};
  },
  computed: {
    ...mapState(["clan", "selectedGroups", "sortField"]),
    allGroups() {
      const groups = new Set();
      for (const [key, value] of Object.entries(this.clan.comparableMembers.groups)) {
        groups.add(value);
      }
      return [...groups];
    },
    selectedGroups: {
      get() {
        return this.$store.state.selectedGroups;
      },
      set(val) {
        this.changeGroups(val);
      },
    },
    days: {
      get() {
        return this.$store.state.days;
      },
      set(val) {
        this.loadDaysAgo(val);
      },
    },
    sort: {
      get() {
        return this.$store.state.sortField;
      },
      set(val) {
        this.changeSort(val);
      },
    },
  },
  methods: {
    ...mapActions({ loadDaysAgo: "SHOW_DIFFERENT_DAYS" }),
    ...mapMutations({ changeSort: "CHANGE_SORT_FIELD", changeGroups: "CHANGE_GROUPS" }),
  },
};
</script>
<style lang="scss" scoped>
/deep/ .switch {
  margin-left: 2em;
}
</style>
