<template>
  <section>
    <div class="tools">
      <b-dropdown scrollable v-model="currentWar" aria-role="list" v-if="currentWar && currentWar.opponent">
        <template #trigger>
          <b-button type="is-danger" icon-right="fa fa-angle-down"> vs {{ currentWar.opponent.name }} </b-button>
        </template>

        <b-dropdown-item v-for="(war, index) in clan.wars" :key="index" :value="war" aria-role="listitem">
          <div class="media">
            <!-- <b-icon class="media-left" :icon="menu.icon"></b-icon> -->
            <div class="media-content">
              <h3>vs {{ war.opponent.name }}</h3>
            </div>
          </div>
        </b-dropdown-item>
      </b-dropdown>
    </div>
    <b-table ref="table" striped mobile-cards :data="currentWar.aggregated" v-if="currentWar">
      <b-table-column field="name" label="Name" v-slot="props" sortable>
        {{ props.row.name }}
      </b-table-column>

      <b-table-column field="tag" label="Tag" v-slot="props" sortable>
        {{ props.row.tag }}
      </b-table-column>

      <b-table-column field="attack1__stars" label="First Attack Stars" v-slot="props" numeric sortable centered>
        <span :class="`stars_${props.row.attack1__stars}`">
          <b-rate v-model="props.row.attack1__stars" icon-pack="fa" icon="star" :max="3" disabled v-if="props.row.attack1__stars != 'na'"> </b-rate>
          <span v-else>-</span>
        </span>
      </b-table-column>

      <b-table-column field="attack1__destructionPercentage" label="First Attack Destruction" v-slot="props" numeric sortable centered>
        {{
          props.row.attack1__destructionPercentage != "na"
            ? Number(props.row.attack1__destructionPercentage / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 0 })
            : "-"
        }}
      </b-table-column>

      <b-table-column field="attack2__stars" label="Second Attack Stars" v-slot="props" numeric sortable centered>
        <span :class="`stars_${props.row.attack2__stars}`">
          <b-rate v-model="props.row.attack2__stars" icon-pack="fa" icon="star" :max="3" disabled v-if="props.row.attack2__stars != 'na'"> </b-rate>
          <span v-else>-</span>
        </span>
      </b-table-column>

      <b-table-column field="attack2__destructionPercentage" label="Second Attack Destruction" v-slot="props" numeric sortable centered>
        {{
          props.row.attack2__destructionPercentage != "na"
            ? Number(props.row.attack2__destructionPercentage / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 0 })
            : "-"
        }}
      </b-table-column>

      <b-table-column field="opponentAttacks" label="Opponent Attacks" v-slot="props" numeric sortable centered>
        {{ props.row.opponentAttacks != "na" ? props.row.opponentAttacks : "-" }}
      </b-table-column>

      <b-table-column field="bestOpponentAttack__stars" label="Best Opponent Stars" v-slot="props" numeric sortable centered>
        <span :class="`stars_${props.row.bestOpponentAttack__stars}`">
          <b-rate v-model="props.row.bestOpponentAttack__stars" icon-pack="fa" icon="star" :max="3" disabled v-if="props.row.bestOpponentAttack__stars != 'na'">
          </b-rate>
          <span v-else>-</span>
        </span>
      </b-table-column>

      <b-table-column field="bestOpponentAttack__destructionPercentage" label="Best Opponent Destruction" v-slot="props" numeric sortable centered>
        {{
          props.row.bestOpponentAttack__destructionPercentage != "na"
            ? Number(props.row.bestOpponentAttack__destructionPercentage / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 0 })
            : "-"
        }}
      </b-table-column>
    </b-table>
  </section>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  components: {},
  name: "ClanWars",
  data() {
    return {
      currentWar: null,
    };
  },
  created() {
    if (this.clan.wars[0] && this.clan.wars[0].opponent) {
      this.currentWar = this.clan.wars[0];
    }
  },
  computed: {
    ...mapState(["clan"]),
  },
  watch: {
    ["clan.wars"](newValue) {
      if (!this.currentWar && newValue && newValue[0].opponent) {
        this.currentWar = newValue[0];
      }
    },
  },
  methods: {},
};
</script>
<style lang="scss" scoped>
.b-table /deep/ th {
  padding: 1em;
}

.rate {
  display: inline-block;
}

.stars_1 .rate /deep/ .rate-item.set-on .icon {
  color: hsl(348, 100%, 61%);
}

.stars_3 .rate /deep/ .rate-item.set-on .icon {
  color: hsl(141, 71%, 48%);
}

.tools {
  width: 100vw;
  position: sticky;
  left: 0;
  padding: 0.6em 1em;
  z-index: 1000;
}
</style>
