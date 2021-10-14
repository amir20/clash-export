<template>
  <section v-if="currentWar && currentWar.opponent">
    <div class="tools">
      <div class="columns">
        <div class="column has-text-centered">
          <div class="columns is-mobile is-inline-flex">
            <div class="column is-narrow">
              <div class="media">
                <div class="media-left">
                  <span class="icon is-medium">
                    <img :src="currentWar.clan.badgeUrls.small" />
                  </span>
                </div>
                <div class="media-content has-text-right">
                  <div>
                    <h3 class="title is-6">{{ currentWar.clan.name }}</h3>
                  </div>
                  <div><b-icon pack="fa" icon="star"></b-icon> {{ currentWar.clan.stars }}</div>
                </div>
              </div>
            </div>
            <div class="column is-narrow has-text-weight-light is-italic">vs</div>
            <div class="column is-narrow">
              <div class="media">
                <div class="media-left">
                  <span class="icon is-medium">
                    <img :src="currentWar.opponent.badgeUrls.small" />
                  </span>
                </div>
                <div class="media-content has-text-left">
                  <div>
                    <h3 class="title is-6">
                      <a :href="currentWar.opponent.slug ? `/clan/${currentWar.opponent.slug}` : `/goto/${encodeURIComponent(currentWar.opponent.tag)}`">
                        {{ currentWar.opponent.name }}
                      </a>
                    </h3>
                  </div>
                  <div><b-icon pack="fa" icon="star"></b-icon> {{ currentWar.opponent.stars }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-narrow">
          <b-dropdown scrollable v-model="currentWar" aria-role="list" :triggers="['hover']" position="is-bottom-left">
            <template #trigger>
              <b-button type="is-danger" icon-right="fa fa-angle-down"> vs {{ currentWar.opponent.name }} </b-button>
            </template>

            <b-dropdown-item v-for="(war, index) in clan.wars" :key="index" :value="war" aria-role="listitem">
              <div class="media">
                <div class="media-left">
                  <span class="icon is-medium">
                    <img :src="war.opponent.badgeUrls.small" />
                  </span>
                </div>
                <div class="media-content">
                  <h3>vs {{ war.opponent.name }}</h3>
                  <small v-if="new Date() < war.startTime"> Starting in {{ war.startTime | formatDistance(false) }}</small>
                  <small v-else-if="new Date() < war.endTime"> Ending in {{ war.endTime | formatDistance(false) }}</small>
                  <small v-else> Ended {{ war.endTime | formatDistance }}</small>
                </div>
              </div>
            </b-dropdown-item>
          </b-dropdown>
        </div>
      </div>
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
          <span v-else>—</span>
        </span>
      </b-table-column>

      <b-table-column field="attack1__destructionPercentage" label="First Attack Destruction" v-slot="props" numeric sortable centered>
        {{
          props.row.attack1__destructionPercentage != "na"
            ? Number(props.row.attack1__destructionPercentage / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 0 })
            : "—"
        }}
      </b-table-column>

      <b-table-column field="attack2__stars" label="Second Attack Stars" v-slot="props" numeric sortable centered>
        <span :class="`stars_${props.row.attack2__stars}`">
          <b-rate v-model="props.row.attack2__stars" icon-pack="fa" icon="star" :max="3" disabled v-if="props.row.attack2__stars != 'na'"> </b-rate>
          <span v-else>—</span>
        </span>
      </b-table-column>

      <b-table-column field="attack2__destructionPercentage" label="Second Attack Destruction" v-slot="props" numeric sortable centered>
        {{
          props.row.attack2__destructionPercentage != "na"
            ? Number(props.row.attack2__destructionPercentage / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 0 })
            : "—"
        }}
      </b-table-column>

      <b-table-column field="opponentAttacks" label="Opponent Attacks" v-slot="props" numeric sortable centered>
        {{ props.row.opponentAttacks != "na" ? props.row.opponentAttacks : "—" }}
      </b-table-column>

      <b-table-column field="bestOpponentAttack__stars" label="Best Opponent Stars" v-slot="props" numeric sortable centered>
        <span :class="`stars_${props.row.bestOpponentAttack__stars}`">
          <b-rate v-model="props.row.bestOpponentAttack__stars" icon-pack="fa" icon="star" :max="3" disabled v-if="props.row.bestOpponentAttack__stars != 'na'">
          </b-rate>
          <span v-else>—</span>
        </span>
      </b-table-column>

      <b-table-column field="bestOpponentAttack__destructionPercentage" label="Best Opponent Destruction" v-slot="props" numeric sortable centered>
        {{
          props.row.bestOpponentAttack__destructionPercentage != "na"
            ? Number(props.row.bestOpponentAttack__destructionPercentage / 100).toLocaleString(undefined, { style: "percent", minimumFractionDigits: 0 })
            : "—"
        }}
      </b-table-column>
    </b-table>
  </section>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import formatDistance from "date-fns/formatDistance";
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
  filters: {
    formatDistance(value, addSuffix = true) {
      if (value instanceof Number) {
        value = new Date(value);
      }
      return formatDistance(value, new Date(), { addSuffix });
    },
  },
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
