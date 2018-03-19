import Vue from "vue";
import Vuex from "vuex";
import camelCase from "lodash/camelCase";
import reduce from "lodash/reduce";
import keyBy from "lodash/keyBy";
import isNumber from "lodash/isNumber";

Vue.use(Vuex);

const state = {
  tag: null,
  loading: true,
  clan: window.__CLAN__ || [],
  previousData: window.__CLAN__ || [],
  days: 7,
  similarClansAvg: {},
  daysSpan: 7,
  sortField: "value"
};

const mutations = {
  setTag(state, tag) {
    state.tag = tag;
  },
  setClan(state, clan) {
    state.clan = clan;
  },
  setPreviousData(state, previousData) {
    state.previousData = previousData;
  },
  setDays(state, days) {
    state.days = days;
  },
  setSimilarClansAvg(state, similarClansAvg) {
    state.similarClansAvg = similarClansAvg;
  },
  startLoading(state) {
    state.loading = true;
  },
  stopLoading(state) {
    state.loading = false;
  },
  setDaysSpan(state, daysSpan) {
    state.daysSpan = daysSpan;
  },
  setSortField(state, field) {
    state.sortField = field;
  }
};

const actions = {
  async fetchClanData({ commit, dispatch, getters: { path } }) {
    const nowPromise = fetch(`${path}.json`);
    const previousPromise = fetch(`${path}.json?daysAgo=${state.days}`);
    commit("stopLoading");

    const previousData = await (await previousPromise).json();
    commit("setPreviousData", previousData);

    const clan = await (await nowPromise).json();
    commit("setClan", clan);

    dispatch("fetchSimilarClansStats");
  },
  async fetchSimilarClansStats({ commit, getters: { path } }) {
    const similarClansAvg = await (await fetch(
      `${path}/similar/avg.json`
    )).json();
    commit("setSimilarClansAvg", similarClansAvg);
  },
  async loadDaysAgo({ commit, getters: { path } }, days) {
    commit("setDays", days);
    commit("startLoading");
    const data = await fetch(`${path}.json?daysAgo=${days}`);
    const previousData = await data.json();
    commit("setPreviousData", previousData);
    commit("stopLoading");
  }
};

// getters are functions
const getters = {
  header({ clan }) {
    if (clan.length > 0) {
      return clan[0].map((column, index) => ({
        label: column,
        field: camelCase(column),
        numeric: index > 1
      }));
    } else {
      return [];
    }
  },
  path({ tag }) {
    return `/clan/${tag.replace("#", "")}`;
  },
  clanAverage(state, { tableData }) {
    const a = c => average(tableData, c);
    return [a("totalDeGrab"), a("totalElixirGrab"), a("totalGoldGrab")];
  },
  tableData(state, getters) {
    if (state.clan.length === 0) {
      return [];
    }
    const data = convertToMap(getters.header, state.clan.slice(1));
    const previousData = convertToMap(
      getters.header,
      state.previousData.slice(1)
    );
    const previousByTag = keyBy(previousData, "tag");

    return data.map(row => {
      const previousRow = previousByTag[row.tag];
      return reduce(
        row,
        (map, value, column) => {
          const delta =
            previousRow && isNumber(value) ? value - previousRow[column] : 0;
          map[column] = { value, delta };
          if (column == "tag") {
            map["id"] = value;
          }
          return map;
        },
        {}
      );
    });
  }
};

const convertToMap = (header, matrix) => {
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
};

const average = (tableData, column) =>
  tableData.reduce((total, player) => total + player[column].delta, 0) /
  tableData.length;

export default new Vuex.Store({
  strict: true,
  state,
  getters,
  actions,
  mutations
});
