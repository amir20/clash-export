<template>
  <div class="hero-body">
    <div class="container is-fluid">
      <div class="columns is-multiline is-centered">
        <div class="column is-12-tablet is-9-desktop is-10-widescreen">
          <div class="columns is-vcentered has-text-centered-mobile">
            <div class="column is-narrow">
              <img :src="clan.badgeUrls.large" width="150" />
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
                        <span class="tag is-light">
                          <i class="fas fa-hashtag mr-1"></i>
                          {{ clan.tag.substr(1) }}
                        </span>
                        <b-tooltip label="Members" position="is-right" type="is-dark" delay="350">
                          <span class="tag is-light">
                            <i class="fas fa-user-friends mr-1"></i>
                            {{ clan.members }}
                          </span>
                        </b-tooltip>
                        <b-tooltip label="Clan Level" position="is-right" type="is-dark" delay="350">
                          <span class="tag is-light">Level {{ clan.clanLevel }}</span>
                        </b-tooltip>
                        <a class="tag is-light" :href="`/country/${clan.location.countryCode.toLowerCase()}`" v-if="clan.location.isCountry">
                          <span class="flag-icon mr-1" :class="`flag-icon-${clan.location.countryCode.toLowerCase()}`"></span>
                          {{ clan.location.name }}
                        </a>
                        <b-tooltip label="Clan War League" position="is-right" type="is-dark" delay="350">
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
                <p class="heading is-tooltip-right tooltip is-tooltip-multiline">Total Trophies <i class="fas fa-info-circle"></i></p>
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
import { mapState } from "vuex";
import LastUpdated from "./LastUpdated";
import ClanField from "./ClanField";
import ClanScore from "./ClanScore";

export default {
  components: {
    TrophyChart: () => import("./TrophyChart"),
    LastUpdated,
    ClanField,
    ClanScore,
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
