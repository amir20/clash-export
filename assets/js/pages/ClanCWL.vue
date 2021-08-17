<template>
  <section>
    <b-table ref="table" striped narrowed mobile-cards :data="cwlData">
      <b-table-column field="name" label="Name" v-slot="props" sortable>
        {{ props.row.name }}
      </b-table-column>

      <b-table-column field="tag" label="Tag" v-slot="props" sortable>
        {{ props.row.tag }}
      </b-table-column>

      <b-table-column field="stars_day_1" label="Day 1" v-slot="props" numeric sortable>
        {{ props.row.stars_day_1 }}
      </b-table-column>

      <b-table-column field="stars_day_2" label="Day 2" v-slot="props" numeric sortable>
        {{ props.row.stars_day_2 }}
      </b-table-column>

      <b-table-column field="stars_day_3" label="Day 3" v-slot="props" numeric sortable>
        {{ props.row.stars_day_3 }}
      </b-table-column>

      <b-table-column field="stars_day_4" label="Day 4" v-slot="props" numeric sortable>
        {{ props.row.stars_day_4 }}
      </b-table-column>

      <b-table-column field="stars_day_5" label="Day 5" v-slot="props" numeric sortable>
        {{ props.row.stars_day_5 }}
      </b-table-column>
      <b-table-column field="stars_day_6" label="Day 6" v-slot="props" numeric sortable>
        {{ props.row.stars_day_6 }}
      </b-table-column>

      <b-table-column field="stars_day_7" label="Day 7" v-slot="props" numeric sortable>
        {{ props.row.stars_day_7 }}
      </b-table-column>

      <b-table-column field="stars_avg" label="Stars Average" v-slot="props" numeric sortable>
        {{ props.row.stars_avg.toLocaleString(undefined, { minimumFractionDigits: 2 }) }}
      </b-table-column>

      <b-table-column field="destruction_day_1" label="Day 1" v-slot="props" numeric sortable>
        {{ Number(props.row.destruction_day_1 / 100).toLocaleString(undefined, { style: "percent" }) }}
      </b-table-column>

      <b-table-column field="destruction_day_2" label="Day 2" v-slot="props" numeric sortable>
        {{ Number(props.row.destruction_day_2 / 100).toLocaleString(undefined, { style: "percent" }) }}
      </b-table-column>

      <b-table-column field="destruction_day_3" label="Day 3" v-slot="props" numeric sortable>
        {{ Number(props.row.destruction_day_3 / 100).toLocaleString(undefined, { style: "percent" }) }}
      </b-table-column>

      <b-table-column field="destruction_day_4" label="Day 4" v-slot="props" numeric sortable>
        {{ Number(props.row.destruction_day_4 / 100).toLocaleString(undefined, { style: "percent" }) }}
      </b-table-column>

      <b-table-column field="destruction_day_5" label="Day 5" v-slot="props" numeric sortable>
        {{ Number(props.row.destruction_day_5 / 100).toLocaleString(undefined, { style: "percent" }) }}
      </b-table-column>
      <b-table-column field="destruction_day_6" label="Day 6" v-slot="props" numeric sortable>
        {{ Number(props.row.destruction_day_6 / 100).toLocaleString(undefined, { style: "percent" }) }}
      </b-table-column>

      <b-table-column field="destruction_day_7" label="Day 7" v-slot="props" numeric sortable>
        {{ Number(props.row.destruction_day_7 / 100).toLocaleString(undefined, { style: "percent" }) }}
      </b-table-column>

      <b-table-column field="destruction_avg" label="Destruction Average" v-slot="props" numeric sortable>
        {{ Number(props.row.destruction_avg / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 1 }) }}
      </b-table-column>
    </b-table>
  </section>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  components: {},
  name: "ClanCWL",
  created() {
    this.fetchClanCWL();
  },
  computed: {
    ...mapState(["clan"]),
    cwlData() {
      return this.clan?.recentCwlGroup?.aggregated ?? [];
    },
  },
  methods: {
    ...mapActions({ fetchClanCWL: "FETCH_CLAN_CWL" }),
  },
};
</script>
<style lang="scss" scoped></style>
