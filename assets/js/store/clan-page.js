import Vue from "vue";
import Vuex from "vuex";
import { event } from "../ga";
import store from "store/dist/store.modern";
import { request } from "../client";
import { gql } from "graphql-request";

Vue.use(Vuex);

const state = {
  loading: true,
  clan: __INITIAL_STATE__,
  days: store.get("days") || 7,
  savedClan: {},
  sortField: store.get("soreField") || "value",
  selectedGroups: store.get("selectedGroups") || ["basic", "war", "trophies"],
};

const mutations = {
  SET_CLAN_DATA(state, { clan }) {
    state.clan = { ...state.clan, ...clan };
  },
  SET_CLAN_CWL(state, { clan }) {
    state.clan = { ...state.clan, ...clan };
  },
  SET_DAYS(state, days) {
    store.set("days", days);
    state.days = days;
  },
  START_LOADING(state) {
    state.loading = true;
  },
  STOP_LOADING(state) {
    state.loading = false;
  },
  SET_SAVED_CLAN(state, { clan }) {
    state.savedClan = clan;
  },
  CHANGE_SORT_FIELD(state, field) {
    store.set("soreField", field);
    state.sortField = field;
  },
  CHANGE_GROUPS(state, groups) {
    store.set("selectedGroups", groups);
    state.selectedGroups = groups;
  },
};

const actions = {
  async FETCH_CLAN_DATA({ commit, dispatch, state: { clan, days } }, { updateWars = true } = { updateWars: true }) {
    commit("START_LOADING");
    dispatch("FETCH_SAVED_CLAN");

    const data = await request(
      gql`
        query GetClan($tag: String!, $days: Int!, $refresh: Int!, $updateWars: Boolean!) {
          clan(tag: $tag, refresh: $refresh, updateWars: $updateWars) {
            name
            clanPoints
            clanVersusPoints
            members
            updatedOn
            clanLevel
            playerStatus
            trophyHistory
            warWins
            warWinRatio
            comparableMembers(deltaDays: $days) {
              header
              mostRecent
              delta
              groups
            }
            warLeague {
              name
            }
            badgeUrls {
              large
            }
            labels {
              id
              name
              iconUrls {
                small
              }
            }
            computed {
              totalDonations
              totalAttackWins
              totalVersusWins
            }
            weekDelta {
              totalTrophies
              totalBhTrophies
              totalDonations
              totalAttackWins
              totalVersusWins
              avgWarStarsPercentile
              avgDonationsPercentile
              avgAttackWinsPercentile
            }
            monthDelta {
              avgCwlStarsPercentile
              avgGamesXpPercentile
            }
            delta(days: $days) {
              avgDeGrab
              avgElixirGrab
              avgGoldGrab
            }
            similar(days: $days) {
              avgDeGrab
              avgElixirGrab
              avgGoldGrab
            }
            recentCwlGroup {
              season
              aggregated
            }
            wars {
              startTime
              endTime
              state
              aggregated
              opponent {
                name
                slug
                tag
                attacks
                stars
                badgeUrls {
                  small
                }
              }
              clan {
                name
                slug
                tag
                attacks
                stars
                badgeUrls {
                  small
                }
              }
            }
          }
        }
      `,
      {
        tag: clan.tag,
        days,
        refresh: 5,
        updateWars: updateWars,
      }
    );
    commit("STOP_LOADING");
    commit("SET_CLAN_DATA", data);
  },
  async FETCH_SAVED_CLAN({ commit, state: { clan, days } }) {
    const savedTag = store.get("lastTag");
    if (savedTag && savedTag !== clan.tag) {
      console.log(`Found saved tag value [${savedTag}].`);
      const data = await request(
        gql`
          query GetSavedClan($tag: String!, $days: Int!) {
            clan(tag: $tag) {
              name
              delta(days: $days) {
                avgDeGrab
                avgElixirGrab
                avgGoldGrab
              }
            }
          }
        `,
        {
          tag: savedTag,
          days,
        }
      );
      commit("SET_SAVED_CLAN", data);
    }
  },
  async SHOW_DIFFERENT_DAYS({ commit, dispatch }, days) {
    event("days-ago", "Change Days", "Days", days);
    commit("SET_DAYS", days);
    dispatch("FETCH_SAVED_CLAN");
    dispatch("FETCH_CLAN_DATA", { updateWars: false });
  },
};

const getters = {};

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});
