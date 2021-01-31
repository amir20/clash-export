<template>
  <div class="hero-body">
    <div class="container is-fluid">
      <div class="columns is-multiline is-centered">
        <div class="column is-12-tablet is-9-desktop is-10-widescreen">
          <div class="columns is-vcentered has-text-centered-mobile">
            <div class="column is-narrow">
              <img :src="clan.badgeUrls.medium" width="128" />
            </div>
            <div class="column">
              <div class="columns">
                <div class="column">
                  <h1 class="title">{{ clan.name }}</h1>
                  <h2 class="subtitle is-6 has-text-weight-light">
                    <span class="has-text-weight-semibold"> <clan-field name="members"></clan-field> members </span>
                    ●
                    <span class="has-text-weight-semibold"> Level <clan-field name="clanLevel"></clan-field></span>
                    <template v-if="clan.location.isCountry">
                      ●
                      <span class="flag-icon" :class="`flag-icon-${clan.location.countryCode.toLowerCase()}`"></span>
                      <a :href="`/country/${clan.location.countryCode.toLowerCase()}`">
                        <span class="has-text-weight-semibold">{{ clan.location.name }}</span>
                      </a>
                    </template>
                    ●
                    <span class="has-text-weight-semibold"> {{ clan.tag }}</span>

                    <!-- {% if 'reddit' in clan.verified_accounts %} ●
                    <span class="has-text-weight-bold">
                      <i class="fab fa-reddit fa-lg reddit-color"></i> Verified Reddit Clan
                      <i class="fas fa-check has-text-success"></i>
                    </span>
                    {% endif %} -->
                    <div class="has-text-weight-light">
                      <i> <last-updated></last-updated> </i>
                    </div>
                  </h2>
                </div>
              </div>
            </div>
          </div>
          <p class="subtitle clan-description" v-html="clan.richDescription"></p>
          <div class="level">
            <!-- Total Trophies -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading is-tooltip-right tooltip is-tooltip-multiline" data-tooltip="Delta is calculated based on data between today and last week.">
                  Total Trophies <i class="fas fa-info-circle"></i>
                </p>
                <p class="title">
                  <clan-field name="clanPoints" class="has-text-weight-light"></clan-field> <br />
                  <clan-field name="weekDelta.totalTrophies" show-plus-sign class="tag" positive-class="is-success" negative-class="is-danger"></clan-field>
                </p>
              </div>
            </div>
            <!-- Total BH Trophies -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Total BH Trophies</p>
                <p class="title">
                  <clan-field name="clanVersusPoints" class="has-text-weight-light"></clan-field> <br />
                  <clan-field name="weekDelta.totalBhTrophies" show-plus-sign class="tag" positive-class="is-success" negative-class="is-danger"></clan-field>
                </p>
              </div>
            </div>
            <!-- Donations -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Donations</p>
                <p class="title">
                  <clan-field name="computed.totalDonations" class="has-text-weight-light"></clan-field> <br />
                  <clan-field name="weekDelta.totalDonations" show-plus-sign class="tag" positive-class="is-success" negative-class="is-danger"></clan-field>
                </p>
              </div>
            </div>
            <!-- Total Wins -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Total Wins</p>
                <p class="title">
                  <clan-field name="computed.totalAttackWins" class="has-text-weight-light"></clan-field> <br />
                  <clan-field name="weekDelta.totalAttackWins" show-plus-sign class="tag" positive-class="is-success" negative-class="is-danger"></clan-field>
                </p>
              </div>
            </div>
            <!-- Total Versus Wins -->
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Total Versus Wins</p>
                <p class="title">
                  <clan-field name="computed.totalVersusWins" class="has-text-weight-light"></clan-field> <br />
                  <clan-field name="weekDelta.totalVersusWins" show-plus-sign class="tag" positive-class="is-success" negative-class="is-danger"></clan-field>
                </p>
              </div>
            </div>
          </div>
          <div class="has-text-centered is-touch-only">
            <a class="button is-info" :href="`clashofclans://action=OpenClanProfile&tag=${clan.tag}`">
              <span class="icon"> <i class="fas fa-external-link-alt"></i></span> <span>Open Clan in Game</span>
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
              <clan-score title="Champion War League" field="monthDelta.avgCwlStarsPercentile"></clan-score>
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
import { mapActions, mapGetters, mapState } from "vuex";

import TrophyChart from "./TrophyChart";
import LastUpdated from "./LastUpdated";
import ClanField from "./ClanField";
import ClanScore from "./ClanScore";

export default {
  components: {
    TrophyChart,
    LastUpdated,
    ClanField,
    ClanScore,
  },
  computed: {
    ...mapState(["clan"]),
  },
};
</script>

<style></style>
