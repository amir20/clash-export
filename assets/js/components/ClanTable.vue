<template>
  <div>
    <section>
       <b-table
            :data="tableData"
            striped
            narrowed
            hoverable
            mobile-cards
            default-sort="currentTrophies.value"
            default-sort-direction="desc"
            :loading="loading">
             <template slot-scope="props">
                <b-table-column v-for="column in header" :label="column.label" :field="`${column.field}.value`" :key="column.field" :numeric="column.numeric" sortable>
                    {{ props.row[column.field].value.toLocaleString() }}
                    <b v-if="column.numeric && props.row[column.field].delta != 0" :class="{up: props.row[column.field].delta > 0, down: props.row[column.field].delta < 0}" :key="props.row[column.field].delta">
                      <i class="fa" :class="{'fa-caret-up': props.row[column.field].delta > 0, 'fa-caret-down': props.row[column.field].delta < 0}" aria-hidden="true"></i> {{ Math.abs(props.row[column.field].delta).toLocaleString() }}
                    </b>
                </b-table-column>
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

export default {
  props: ["tag", "name", "players"],
  data() {
    return {
      loading: true,
      clan: null,
      previousData: null,
      days: 7,
    };
  },
  created() {
    this.clan = this.players;
    this.previousData = this.players;
    this.fetchData();
    this.$bus.$on("days-changed-event", days => {
      this.loadDaysAgo(days);
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
    }
  }
};
</script>

<style scoped>
.b-table {
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
  }
}

section {
  overflow-y: scroll;
}
</style>
