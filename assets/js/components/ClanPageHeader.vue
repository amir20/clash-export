<template>
  <div class="hero-body">
    <div class="container is-fluid">
      <div class="columns is-multiline is-centered">
        <div class="column is-12-tablet is-9-desktop is-10-widescreen">
          <div class="columns is-vcentered has-text-centered-mobile">
            <div class="column is-narrow">
              <img :src="clan.badgeUrls.large" width="180" height="180" />
            </div>
            <div class="column">
              <div class="columns">
                <div class="column">
                  <h1 class="title is-marginless">{{ clan.name }}</h1>
                  <div class="has-text-weight-light">
                    <i> <last-updated></last-updated> </i>
                  </div>
                  <div class="columns mt-2 mb-0">
                    <div class="column is-narrow pt-0 pb-0">
                      <div class="tags is-centered">
                        <clan-tag :value="clan.tag"></clan-tag>
                        <b-tooltip label="Members" position="is-right" type="is-dark" :delay="350">
                          <span class="tag is-light">
                            <i class="fas fa-user-friends mr-1"></i>
                            {{ clan.members }}
                          </span>
                        </b-tooltip>
                        <b-tooltip label="Clan Level" position="is-right" type="is-dark" :delay="350">
                          <span class="tag is-light">Level {{ clan.clanLevel }}</span>
                        </b-tooltip>
                        <a class="tag is-light" :href="`/country/${clan.location.countryCode.toLowerCase()}`" v-if="clan.location.isCountry">
                          <span class="flag-icon mr-1" :class="`flag-icon-${clan.location.countryCode.toLowerCase()}`"></span>
                          {{ clan.location.name }}
                        </a>
                        <b-tooltip label="Clan War League" position="is-right" type="is-dark" :delay="350">
                          <span class="tag is-light">
                            {{ clan.warLeague.name }}
                          </span>
                        </b-tooltip>
                      </div>
                    </div>
                  </div>
                  <div class="columns mt-2 mb-0">
                    <div class="column is-narrow pt-0 pb-0">
                      <div class="tags is-centered">
                        <span class="tag is-danger is-light" v-for="label in clan.labels" :key="label.id">
                          <img :src="label.iconUrls.small" width="20" class="mr-1" />
                          {{ label.name }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="subtitle is-6 has-text-weight-light">
                    <!-- {% if 'reddit' in clan.verified_accounts %} ●
                    <span class="has-text-weight-bold">
                      <i class="fab fa-reddit fa-lg reddit-color"></i> Verified Reddit Clan
                      <i class="fas fa-check has-text-success"></i>
                    </span>
                    {% endif %} -->
                  </div>
                </div>
              </div>
            </div>
          </div>
          <p class="subtitle clan-description" v-html="clan.richDescription"></p>
          <div class="level">
            <!-- Total Trophies -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Total Trophies</p>
                <p class="title has-text-weight-light">
                  <clan-field :value="clan.clanPoints"></clan-field>
                </p>
              </div>
            </div>
            <!-- Total BH Trophies -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Total BH Trophies</p>
                <p class="title has-text-weight-light">
                  <clan-field :value="clan.clanVersusPoints"></clan-field>
                </p>
              </div>
            </div>
            <!-- Donations -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Donations</p>
                <p class="title has-text-weight-light">
                  <clan-field :value="clan.computed.totalDonations"></clan-field>
                </p>
              </div>
            </div>
            <!-- War Wins -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">War Wins</p>
                <p class="title has-text-weight-light">
                  <clan-field :value="clan.warWins"></clan-field>
                </p>
              </div>
            </div>
            <!-- Warn Win Ratio -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">War Win Ratio</p>
                <p class="title has-text-weight-light">
                  <clan-field :value="clan.warWinRatio" :locale-style="{ style: 'percent' }"></clan-field>
                </p>
              </div>
            </div>
          </div>
          <div class="has-text-centered is-touch-only">
            <a class="button is-info" :href="`clashofclans://action=OpenClanProfile&tag=${clan.tag}`">
              <span class="icon"> <i class="fas fa-external-link-alt"></i></span>
              <span>Open Clan in Game</span>
            </a>
          </div>
          <div class="is-hidden-mobile">
            <trophy-chart></trophy-chart>
          </div>
        </div>

        <div class="column is-5-tablet is-3-desktop is-2-widescreen">
          <div class="panel is-primary scorecard">
            <h3 class="panel-heading has-text-centered">Clan Scorecard&trade;</h3>
            <div class="panel-block">
              <clan-score title="Clan War League" field="monthDelta.avgCwlStarsPercentile"></clan-score>
            </div>
            <div class="panel-block">
              <clan-score title="Clan Games" field="monthDelta.avgGamesXpPercentile"></clan-score>
            </div>
            <div class="panel-block">
              <clan-score title="Clan Wars" field="weekDelta.avgWarStarsPercentile"></clan-score>
            </div>
            <div class="panel-block">
              <clan-score title="Donations" field="weekDelta.avgDonationsPercentile"></clan-score>
            </div>
            <div class="panel-block">
              <clan-score title="Attacks Won" field="weekDelta.avgAttackWinsPercentile"></clan-score>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import LastUpdated from "./LastUpdated";
import ClanField from "./ClanField";
import ClanScore from "./ClanScore";
import ClanTag from "./ClanTag";

export default {
  components: {
    TrophyChart: () => import("./TrophyChart"),
    LastUpdated,
    ClanField,
    ClanScore,
    ClanTag,
  },
  computed: {
    ...mapState(["clan"]),
  },
};
</script>

<style lang="scss" scoped>
a.tag {
  text-decoration: underline;
}
</style>
