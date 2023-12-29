<template>
  <section>
    <b-table ref="table" striped mobile-cards :data="cwlData">
      <b-table-column field="name" label="Name" v-slot="props" sortable>
        {{ props.row.name }}
      </b-table-column>

      <b-table-column field="tag" label="Tag" v-slot="props" sortable>
        {{ props.row.tag }}
      </b-table-column>

      <b-table-column
        :field="`stars_day_${i}`"
        :label="`Day ${i}`"
        v-slot="props"
        numeric
        sortable
        centered
        v-for="i in [1, 2, 3, 4, 5, 6, 7]"
        :key="'stars' + i"
      >
        <span class="stars" :class="`stars_${props.row[`stars_day_${i}`]}`">
          <b-rate v-model="props.row[`stars_day_${i}`]" icon-pack="fa" icon="star" :max="3" disabled v-if="props.row[`stars_day_${i}`] != 'na'"> </b-rate>
          <span v-else>—</span>
        </span>
      </b-table-column>

      <b-table-column field="stars_avg" label="Stars Average" v-slot="props" numeric sortable centered>
        {{ props.row.stars_avg.toLocaleString(undefined, { minimumFractionDigits: 2 }) }}
      </b-table-column>

      <b-table-column
        :field="`destruction_day_${i}`"
        :label="`Day ${i}`"
        v-slot="props"
        numeric
        sortable
        centered
        v-for="i in [1, 2, 3, 4, 5, 6, 7]"
        :key="'destruction' + i"
      >
        {{
          props.row[`destruction_day_${i}`] != "na"
            ? Number(props.row[`destruction_day_${i}`] / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 0 })
            : "—"
        }}
      </b-table-column>

      <b-table-column field="destruction_avg" label="Destruction Average" v-slot="props" numeric sortable centered>
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
  computed: {
    ...mapState(["clan"]),
    cwlData() {
      return this.clan?.recentCwlGroup?.aggregated ?? [];
    },
  },
  methods: {},
};
</script>
<style lang="scss" scoped>
.b-table :deep(th) {
  padding: 1em;
}

.stars_1 .rate :deep(.rate-item.set-on .icon) {
  color: hsl(348, 100%, 61%);
}

.stars_3 .rate :deep(.rate-item.set-on .icon) {
  color: hsl(141, 71%, 48%);
}
</style>
