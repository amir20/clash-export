import Vue from "vue";
import Vuex from "vuex";
import camelCase from "lodash/camelCase";
import reduce from "lodash/reduce";
import keyBy from "lodash/keyBy";
import { event } from "../ga";
import store from "store/dist/store.modern";
import { request } from "../client";
import { gql } from "graphql-request";

Vue.use(Vuex);

const state = {
  loading: true,
  clan: __INITIAL_STATE__,
  days: 7,
  savedClan: {},
  sortField: "value",
};

const mutations = {
  SET_CLAN_DATA(state, { clan }) {
    state.clan = { ...state.clan, ...clan };
  },
  SET_CLAN_CWL(state, { clan }) {
    state.clan = { ...state.clan, ...clan };
  },
  SET_DAYS(state, days) {
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
    state.sortField = field;
  },
};

const actions = {
  async FETCH_CLAN_DATA({ commit, dispatch, state: { clan, days } }) {
    commit("START_LOADING");
    dispatch("FETCH_SAVED_CLAN");

    const data = await request(
      gql`
        query GetClan($tag: String!, $days: Int!, $refresh: Int!) {
          clan(tag: $tag, refresh: $refresh) {
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
                badgeUrls {
                  large
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
      }
    );
    commit("STOP_LOADING");
    commit("SET_CLAN_DATA", data);
    dispatch("FETCH_WARS");
  },
  async FETCH_WARS({ commit, state: { clan } }) {
    try {
      commit("START_LOADING");
      const data = await request(
        gql`
          query GetClanCWL($tag: String!, $updateWars: Boolean!) {
            clan(tag: $tag, updateWars: $updateWars) {
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
                  badgeUrls {
                    large
                  }
                }
              }
            }
          }
        `,
        {
          tag: clan.tag,
          updateWars: true,
        }
      );
      commit("SET_CLAN_CWL", data);
    } catch (error) {
      console.error(error);
    } finally {
      commit("STOP_LOADING");
    }
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
  async SHOW_DIFFERENT_DAYS({ commit, dispatch, state: { clan } }, days) {
    event("days-ago", "Change Days", "Days", days);
    commit("SET_DAYS", days);
    dispatch("FETCH_SAVED_CLAN");

    commit("START_LOADING");
    const data = await request(
      gql`
        query ChangeClanHistoric($tag: String!, $days: Int!) {
          clan(tag: $tag) {
            comparableMembers(deltaDays: $days) {
              header
              mostRecent
              delta
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
          }
        }
      `,
      {
        tag: clan.tag,
        days,
      }
    );
    commit("STOP_LOADING");
    commit("SET_CLAN_DATA", data);
  },
};

const getters = {};

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});
