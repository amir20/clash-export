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
            :opened-detailed="openDetails"
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
                      <span :class="{'fa-caret-up': props.row[column.field].delta > 0 , 'fa-caret-down': props.row[column.field].delta < 0}" class="fa-sm fa"></span>
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
import debounce from "lodash/debounce";

const fixPage = debounce(table => {
  const items = [
    document.querySelector(".hero.is-warning.is-bold"),
    document.querySelector("nav.navbar"),
    document.querySelector("footer")
  ];
  const width = table.$el.querySelector("table").offsetWidth;
  items.forEach(item => (item.style.width = `${width}px`));
  items.forEach(item => (item.style.paddingRight = `calc(${width}px - 100vw)`));
}, 500);

export default {
  props: ["tag", "name", "oldestDays"],
  components: {
    PlayerComparison
  },
  data() {
    return {
      selected: null,
      openDetails: []
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
  updated() {
    fixPage(this.$refs.table);
  },
  computed: {
    ...mapState(["loading", "sortField", "similarClansAvg"]),
    ...mapGetters(["path", "header", "tableData"])
  },
  watch: {
    sortField(newValue) {
      const column = this.$refs.table.currentSortColumn;
      this.$nextTick(() => this.$refs.table.sort(column, true));
    },
    similarClansAvg(newValue) {
      if (newValue && newValue.gold_grab > 0) {
        this.openDetails = [this.tableData[0].id];
      }
    }
  },
  methods: {
    ...mapMutations(["setTag", "setDaysSpan"]),
    ...mapActions(["fetchClanData", "loadDaysAgo"])
  }
};
</script>

<style scoped>
.b-table {
  & >>> thead th {
    position: sticky;
    top: 0;
    z-index: 11;
    background-color: #00d1b2;
    color: #fff;
  }

  & >>> .table {
    &.is-striped tbody tr:not(.is-selected):nth-child(even) {
      background-color: #eee;
    }

    & tr.is-selected {
      background-color: #555;
    }
  }

  & >>> table {
    font-size: 90%;
  }

  & >>> b {
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
</style>

<style>
html {
  overflow: unset;
}

.navbar {
  z-index: 99;
}
</style>
