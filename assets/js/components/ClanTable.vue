<template>
  <div>
    <section>
       <b-table
            ref="table"
            :data="tableData"
            striped
            narrowed
            hoverable
            mobile-cards
            detail-key="id"
            detailed
            default-sort="currentTrophies.value"
            default-sort-direction="desc"
            :loading="loading"
            :selected.sync="selected"
            focusable>
             <template slot-scope="props">
                <b-table-column v-for="column in header"
                                :label="column.label"
                                :field="`${column.field}.${sortField}`"
                                :key="column.field"
                                :numeric="column.numeric"
                                sortable>
                    {{ props.row[column.field].value.toLocaleString() }}
                    <b v-show="column.numeric && props.row[column.field].delta != 0" :class="{up: props.row[column.field].delta > 0, down: props.row[column.field].delta < 0}" :key="props.row[column.field].delta">
                      <b-icon :icon="props.row[column.field].delta > 0 ? 'caret-up' : 'caret-down'" size="is-small"></b-icon> 
                      {{ Math.abs(props.row[column.field].delta).toLocaleString() }}
                    </b>
                </b-table-column>
            </template>
            <template slot="detail" slot-scope="props">
              <player-comparison :player-data="props.row" :all-data="tableData"></player-comparison>
            </template>
        </b-table>
    </section>
  </div>
</template>

<script>
import camelCase from "lodash/camelCase";
import reduce from "lodash/reduce";
import keyBy from "lodash/keyBy";
import isNumber from "lodash/isNumber";
import PlayerComparison from "./PlayerComparison";

export default {
  props: ["tag", "name", "players", "oldestDays"],
  components: {
    PlayerComparison
  },
  data() {
    return {
      loading: true,
      clan: null,
      previousData: null,
      days: 7,
      selected: null,
      sortField: "value"
    };
  },
  created() {
    this.clan = this.players;
    this.previousData = this.players;
    this.fetchData();
    this.$bus.$on("days-changed-event", days => this.loadDaysAgo(days));
    this.$bus.$on("sort-changed-event", sort => this.changedSortField(sort));

    if (this.oldestDays < 3) {
      this.showNoDataMessage();
      this.$nextTick(() => {
        this.$bus.$emit("days-changed-event", 1);
      });
    }
    this.$nextTick(() => {
      this.$bus.$emit("days-of-data", this.oldestDays);
    });
  },
  computed: {
    tableData() {
      const data = this.convertToMap(this.clan.slice(1));
      const previousData = this.convertToMap(this.previousData.slice(1));
      const previousByTag = keyBy(previousData, "tag");

      return data.map(row => {
        const previousRow = previousByTag[row.tag];
        return reduce(
          row,
          (map, value, column) => {
            const delta =
              previousRow && isNumber(value) ? value - previousRow[column] : 0;
            map[column] = { value, delta };
            if (column == "tag") {
              map["id"] = value;
            }
            return map;
          },
          {}
        );
      });
    },
    header() {
      return this.clan[0].map((column, index) => ({
        label: column,
        field: camelCase(column),
        numeric: index > 1
      }));
    },
    path() {
      return `/clan/${this.tag.replace("#", "")}`;
    }
  },
  methods: {
    async fetchData() {
      const nowPromise = fetch(`${this.path}.json`);
      const previousPromise = fetch(`${this.path}.json?daysAgo=${this.days}`);
      this.loading = false;

      this.previousData = await (await previousPromise).json();
      this.clan = await (await nowPromise).json();
    },
    async loadDaysAgo(days) {
      this.days = days;
      this.loading = true;
      const data = await fetch(`${this.path}.json?daysAgo=${days}`);
      this.previousData = await data.json();
      this.loading = false;
    },
    changedSortField(sort) {
      if (this.sortField != sort) {
        this.sortField = sort;
        const column = this.$refs.table.currentSortColumn;
        this.$nextTick(() => this.$refs.table.sort(column, true));
      }
    },
    convertToMap(matrix) {
      const header = this.header;
      return matrix.map(row => {
        return reduce(
          row,
          (map, value, columnIndex) => {
            map[header[columnIndex].field] = value;
            return map;
          },
          {}
        );
      });
    },
    showNoDataMessage() {
      this.$snackbar.open({
        message:
          "Hey stranger! This is the first time I am seeing your clan and so it will take a while to collect historical data. Come back again in a few days to see your updated stats.",
        type: "is-warning",
        position: "is-bottom-left",
        actionText: "Got it",
        duration: 20000
      });
    }
  }
};
</script>

<style scoped>
.b-table {
  &>>>.table {
    &.is-striped tbody tr:not(.is-selected):nth-child(even) {
      background-color: #eee;
    }

    & tr.is-selected {
      background-color: #555;
    }
  }

  &>>>table {
    font-size: 90%;
  }

  &>>>thead {
    background-color: #00d1b2;

    & th {
      color: #fff;
    }
  }

  &>>>b {
    white-space: nowrap;
    display: block;
    line-height: 1;
    margin-top: 5px;
    font-size: 95%;
    &.up {
      color: #23d160;
    }
    &.down {
      color: #ff3860;
    }

    & .icon > svg {
      height: auto;
    }
  }
}

section {
  overflow-y: scroll;
}
</style>
