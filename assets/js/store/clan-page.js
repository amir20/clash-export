import Vue from "vue";
import Vuex from "vuex";
import camelCase from "lodash/camelCase";
import reduce from "lodash/reduce";
import keyBy from "lodash/keyBy";
import { event } from "../ga";
import store from "store/dist/store.modern";
import { apolloClient } from "../client";
import { gql } from "apollo-boost";

Vue.use(Vuex);

const state = {
  loading: true,
  clan: window.__INITIAL_STATE__,
  days: 7,
  savedClan: {},
  sortField: "value"
};

const mutations = {
  SET_CLAN_DATA(state, { clan }) {
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
  }
};

const actions = {
  async FETCH_CLAN_DATA({ commit, dispatch, state: { clan, days } }) {
    dispatch("FETCH_SAVED_CLAN");
    commit("STOP_LOADING");
    const { data } = await apolloClient.query({
      query: gql`
        query GetClan($tag: String!, $days: Int!, $refresh: Boolean!) {
          clan(tag: $tag, refresh: $refresh) {
            name
            clanPoints
            clanVersusPoints
            members
            updatedOn
            playerStatus
            recentData: playerMatrix
            historicData: playerMatrix(days: $days)
            computed {
              totalDonations
              totalAttackWins
              totalVersusWins
            }
            weekDelta {
              totalTrophies
              totalVersusWins
              totalDonations
              totalAttackWins
              totalVersusWins
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
      variables: {
        tag: clan.tag,
        days,
        refresh: true
      }
    });

    commit("SET_CLAN_DATA", data);
  },
  async FETCH_SAVED_CLAN({ commit, state: { clan, days } }) {
    const savedTag = store.get("lastTag");
    if (savedTag && savedTag !== clan.tag) {
      console.log(`Found saved tag value [${savedTag}].`);
      const { data } = await apolloClient.query({
        query: gql`
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
        variables: {
          tag: savedTag,
          days
        }
      });
      commit("SET_SAVED_CLAN", data);
    }
  },
  async SHOW_DIFFERENT_DAYS(
    {
      commit,
      dispatch,
      state: { clan }
    },
    days
  ) {
    event("days-ago", "Change Days", "Days", days);
    commit("SET_DAYS", days);
    dispatch("FETCH_SAVED_CLAN");

    commit("START_LOADING");
    const { data } = await apolloClient.query({
      query: gql`
        query ChangeClanHistoric($tag: String!, $days: Int!) {
          clan(tag: $tag) {
            historicData: playerMatrix(days: $days)
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
      variables: {
        tag: clan.tag,
        days
      }
    });
    commit("STOP_LOADING");
    commit("SET_CLAN_DATA", data);
  }
};

const getters = {
  header({ clan }) {
    return clan.recentData[0].map(column => ({
      label: column,
      field: camelCase(column),
      numeric: !isNonNumericColumns(camelCase(column))
    }));
  },
  tableData({ clan }, getters) {
    const data = convertToMap(getters.header, clan.recentData.slice(1));
    const previousData = convertToMap(getters.header, clan.historicData.slice(1));
    const previousByTag = keyBy(previousData, "tag");

    return data.map(row => {
      const previousRow = previousByTag[row.tag];
      return reduce(
        row,
        (map, value, column) => {
          const delta = previousRow && !isNonNumericColumns(column) ? value - previousRow[column] : 0;
          map[column] = { value, delta };
          if (column === "tag") {
            map["id"] = value;
          }
          return map;
        },
        {}
      );
    });
  }
};

function convertToMap(header, matrix) {
  return matrix.map(row => {
    return reduce(
      row,
      (map, value, columnIndex) => {
        map[header[columnIndex].field] = value;
        return map;
      },
      {}
    );
  });
}

const isNonNumericColumns = key => key == "tag" || key == "name";

export default new Vuex.Store({
  strict: true,
  state,
  getters,
  actions,
  mutations
});
