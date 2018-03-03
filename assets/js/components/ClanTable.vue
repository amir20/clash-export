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
              <player-comparison :player-data="props.row"></player-comparison>
            </template>
        </b-table>
    </section>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";
import PlayerComparison from "./PlayerComparison";

export default {
  props: ["tag", "name", "players", "oldestDays", "clusterLabel"],
  components: {
    PlayerComparison
  },
  data() {
    return {
      selected: null
    };
  },
  created() {
    this.setTag(this.tag);
    this.setDaysSpan(this.oldestDays);
    this.setClan(this.players);
    this.setPreviousData(this.players);
    this.fetchClanData(this.clusterLabel);

    if (this.oldestDays < 3) {
      this.setDaysSpan(1);
    }
  },
  computed: {
    ...mapState(["loading", "sortField"]),
    ...mapGetters(["path", "header", "tableData"])
  },
  watch: {
    sortField(newValue) {
      const column = this.$refs.table.currentSortColumn;
      this.$nextTick(() => this.$refs.table.sort(column, true));
    }
  },
  methods: {
    ...mapMutations(["setClan", "setPreviousData", "setTag", "setDaysSpan"]),
    ...mapActions(["fetchClanData", "loadDaysAgo"])
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
