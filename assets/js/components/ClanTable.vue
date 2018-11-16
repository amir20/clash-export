<template>
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
      :opened-detailed="openDetails"
      @details-open="row => gaEvent('open-player-details', 'Click Player Details', 'Player Tag', row.tag.value)"
      @sort="column => gaEvent('sort-players', 'Sort Column', 'Column', column)"
      @click="onRowclicked"
    >
      <template slot-scope="props">
        <b-table-column
          v-for="column in header"
          :label="column.label"
          :field="`${column.field}.${sortField}`"
          :key="column.field"
          :numeric="column.numeric"
          sortable
        >
          {{ props.row[column.field].value.toLocaleString() }}
          <span
            v-if="column.field == 'name' && playersStatus[props.row.tag.value]"
            class="tag is-uppercase"
            :class="playersStatus[props.row.tag.value]"
            >{{ playersStatus[props.row.tag.value] }}</span
          >
          <b
            v-if="column.numeric && props.row[column.field].delta != 0"
            :class="{
              up: props.row[column.field].delta > 0,
              down: props.row[column.field].delta < 0
            }"
            :key="props.row[column.field].delta"
          >
            <span
              :class="{
                'fa-caret-up': props.row[column.field].delta > 0,
                'fa-caret-down': props.row[column.field].delta < 0
              }"
              class="fa-sm fa"
            ></span>
            {{ Math.abs(props.row[column.field].delta).toLocaleString() }}
          </b>
        </b-table-column>
      </template>
      <template slot="detail" slot-scope="props">
        <player-comparison :player-data="props.row"></player-comparison>
      </template>
    </b-table>
  </section>
</template>

<script>
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";
import PlayerComparison from "./PlayerComparison";
import formatDistance from "date-fns/formatDistance";
import { gaMixin } from "../ga";

export default {
  mixins: [gaMixin],
  props: ["tag", "name", "oldestDays"],
  components: {
    PlayerComparison
  },
  data() {
    return {
      selected: null,
      openDetails: null
    };
  },
  created() {
    this.setTag(this.tag);
    this.setDaysSpan(this.oldestDays);
    this.fetchClanData();

    if (this.oldestDays < 3) {
      this.setDaysSpan(1);
    }
  },
  computed: {
    ...mapState(["loading", "sortField", "similarClansAvg", "apiError", "playersStatus"]),
    ...mapGetters(["path", "header", "tableData", "lastUpdated"])
  },
  watch: {
    sortField(newValue) {
      const column = this.$refs.table.currentSortColumn;
      this.$nextTick(() => this.$refs.table.sort(column, true));
    },
    tableData(newValue) {
      if (newValue && newValue.length > 0 && this.openDetails == null) {
        this.openDetails = [this.tableData[0].id];
      }
    },
    apiError(newValue, oldValue) {
      if (newValue && !oldValue && newValue.status >= 500) {
        const last = formatDistance(this.lastUpdatedAgo, new Date(), {
          addSuffix: true
        });
        this.$snackbar.open({
          message: `Well Chief, this is embarrassing. It seems Clash of Clans' API is not responding right now. This clan was last updated ${last}. I'll keep checking for updates even after you leave.`,
          type: "is-warning",
          position: "is-top",
          duration: 20000
        });
      }
    }
  },
  methods: {
    ...mapMutations(["setTag", "setDaysSpan"]),
    ...mapActions(["fetchClanData", "loadDaysAgo"]),
    onRowclicked(row) {
      this.gaEvent("click-row", "Click Player Row", "Row Tag", row.tag.value);
      if (this.openDetails.indexOf(row.id) === -1) {
        this.openDetails.push(row.id);
      } else {
        this.openDetails.splice(this.openDetails.indexOf(row.id), 1);
      }
    }
  }
};
</script>

<style scoped>
.b-table {
  & /deep/ thead th {
    position: sticky;
    top: 0;
    z-index: 11;
    background-color: #00d1b2;
    color: #fff;
  }

  & /deep/ td[data-label="Name"] {
    white-space: nowrap;
  }

  & /deep/ .table {
    &.is-striped tbody tr:not(.is-selected):nth-child(even) {
      background-color: #eee;
    }

    tr.detail .detail-container {
      padding: 0;
    }
  }

  & /deep/ table {
    font-size: 90%;
  }

  & /deep/ b {
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

  & .tag {
    font-size: 10px;

    &.inactive {
      background-color: #ffdd57;
      color: rgba(0, 0, 0, 0.7);
    }

    &.mvp {
      background-color: #ff3860;
      color: #fff;
    }

    &.new {
      background-color: #23d160;
      color: #fff;
    }
  }
}
</style>
