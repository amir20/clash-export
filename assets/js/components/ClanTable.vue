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
      :opened-detailed="openDetails"
      @details-open="(row) => gaEvent('open-player-details', 'Click Player Details', 'Player Tag', row.tag.value)"
      @sort="(column) => gaEvent('sort-players', 'Sort Column', 'Column', column)"
      @click="onRowClicked"
    >
      <b-table-column
        v-for="column in header"
        :label="column.label"
        :field="`${column.field}.${sortField}`"
        :key="column.field"
        :numeric="column.numeric"
        sortable
        v-slot="props"
      >
        {{ props.row[column.field].value.toLocaleString() }}
        <span
          v-if="column.field == 'name' && clan.playerStatus[props.row.tag.value]"
          class="tag is-uppercase"
          :class="clan.playerStatus[props.row.tag.value]"
          >{{ clan.playerStatus[props.row.tag.value] }}</span
        >
        <b
          v-if="column.numeric && props.row[column.field].delta != 0"
          :class="{
            up: props.row[column.field].delta > 0,
            down: props.row[column.field].delta < 0,
          }"
          :key="props.row[column.field].delta"
        >
          <span
            :class="{
              'fa-caret-up': props.row[column.field].delta > 0,
              'fa-caret-down': props.row[column.field].delta < 0,
            }"
            class="fa-sm fa"
          ></span>
          {{ Math.abs(props.row[column.field].delta).toLocaleString() }}
        </b>
      </b-table-column>

      <template slot="detail" slot-scope="props">
        <player-comparison :player-data="props.row"></player-comparison>
      </template>
    </b-table>
  </section>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import PlayerComparison from "./PlayerComparison";
import { gaMixin } from "../ga";
import UserMixin from "../user";

export default {
  mixins: [gaMixin, UserMixin],
  props: ["tag", "name", "oldestDays"],
  components: {
    PlayerComparison,
  },
  data() {
    return {
      selected: null,
      openDetails: [],
    };
  },
  created() {
    document.addEventListener("visibilitychange", this.handleVisibilityChange, false);
  },
  mounted() {
    if (this.hasUser) {
      this.openDetails = [this.userTag];
    } else if (this.tableData.length > 0) {
      this.openDetails = [this.tableData[0].id];
    }
  },
  beforeDestroy() {
    document.removeEventListener("visibilitychange");
  },
  computed: {
    ...mapState(["sortField", "clan"]),
    ...mapGetters(["header", "tableData"]),
  },
  watch: {
    sortField(newValue) {
      const column = this.$refs.table.currentSortColumn;
      this.$nextTick(() => this.$refs.table.sort(column, true));
    },
  },
  methods: {
    ...mapActions({ fetchClanData: "FETCH_CLAN_DATA" }),
    onRowClicked(row) {
      this.gaEvent("click-row", "Click Player Row", "Row Tag", row.tag.value);
      if (this.openDetails.indexOf(row.id) === -1) {
        this.openDetails.push(row.id);
      } else {
        this.openDetails.splice(this.openDetails.indexOf(row.id), 1);
      }
    },
    handleVisibilityChange() {
      if (!document.hidden) {
        this.fetchClanData();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
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
