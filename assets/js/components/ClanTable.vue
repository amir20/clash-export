<template>
  <section>
    <b-table
      ref="table"
      :data="tableData"
      striped
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
      v-if="clan.comparableMembers"
    >
      <b-table-column
        v-for="key in Object.keys(clan.comparableMembers.header)"
        :label="clan.comparableMembers.header[key]"
        :field="`${key}.${sortField}`"
        :key="key"
        :numeric="isNumeric(key)"
        sortable
        v-slot="props"
        :visible="isVisible(key)"
      >
        {{ formatNumber(key, props.row[key].value) }}
        <span v-if="key == 'name' && clan.playerStatus[props.row.tag.value]" class="tag is-uppercase" :class="clan.playerStatus[props.row.tag.value]">{{
          clan.playerStatus[props.row.tag.value]
        }}</span>
        <b
          v-if="isNumeric(key) && props.row[key].delta != 0"
          :class="{
            up: props.row[key].delta > 0,
            down: props.row[key].delta < 0,
          }"
          :key="props.row[key].delta"
        >
          <span
            :class="{
              'fa-caret-up': props.row[key].delta > 0,
              'fa-caret-down': props.row[key].delta < 0,
            }"
            class="fa-sm fa"
          ></span>
          {{ formatNumber(key, props.row[key].delta) }}
        </b>
      </b-table-column>

      <template slot="detail" slot-scope="props">
        <player-comparison :player-data="props.row"></player-comparison>
      </template>
    </b-table>
    <notification></notification>
  </section>
</template>

<script>
import { mapState } from "vuex";
import Notification from "./Notification";
import { gaMixin } from "../ga";
import UserMixin from "../user";

const compactFormatter = Intl.NumberFormat("en", { notation: "compact" });

export default {
  mixins: [gaMixin, UserMixin],
  props: [],
  components: {
    PlayerComparison: () => import("./PlayerComparison"),
    Notification,
  },
  data() {
    return {
      selected: null,
      openDetails: [],
    };
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
    ...mapState(["sortField", "clan", "selectedGroups"]),
    tableData() {
      const { mostRecent, delta } = this.clan.comparableMembers;
      return mostRecent.map((player) => {
        const row = {};
        for (const [key, value] of Object.entries(player)) {
          const deltaValue = delta[player.tag][key] ?? 0;
          row[key] = { value, delta: deltaValue };
        }
        row.id = player.tag;
        return row;
      });
    },
    visibleColumns() {
      const visible = {};
      for (const group of this.selectedGroups) {
        visible[group] = true;
      }
      return visible;
    },
  },
  watch: {
    sortField(newValue) {
      const column = this.$refs.table.currentSortColumn;
      this.$nextTick(() => this.$refs.table.sort(column, true));
    },
  },
  methods: {
    onRowClicked(row) {
      this.gaEvent("click-row", "Click Player Row", "Row Tag", row.tag.value);
      if (this.openDetails.indexOf(row.id) === -1) {
        this.openDetails.push(row.id);
      } else {
        this.openDetails.splice(this.openDetails.indexOf(row.id), 1);
      }
    },
    isNumeric(key) {
      return key != "tag" && key != "name";
    },
    formatNumber(key, data) {
      if (data == "na") return "—";
      switch (key) {
        case "tag":
        case "name":
          return data;
        case "avgWarDestruction":
        case "activityScore":
          return (data / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 0 });
        default:
          return compactFormatter.format(data);
      }
    },
    isVisible(key) {
      const group = this.clan.comparableMembers.groups[key];
      return this.visibleColumns[group] === true;
    },
  },
};
</script>
<style lang="scss" scoped>
.b-table /deep/ {
  th {
    padding: 1em;
  }
  td[data-label="Name"] {
    white-space: nowrap;
  }

  tr.detail .detail-container {
    padding: 0 !important;
  }

  b {
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

  .tag {
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

<style lang="scss">
.b-table {
  .table {
    thead th {
      position: sticky;
      top: 0;
      z-index: 11;
      background-color: #00d1b2;
      color: #fff;
    }

    &.is-striped tbody tr:not(.is-selected):nth-child(even) {
      background-color: #eee;
    }

    th.is-sortable {
      padding-right: 1em;

      .is-relative {
        padding-left: 0.2em;
      }
    }
  }

  table {
    font-size: 90%;
  }
}
</style>
