import Vue from "vue";
import Vuex from "vuex";
import camelCase from "lodash/camelCase";
import reduce from "lodash/reduce";
import keyBy from "lodash/keyBy";
import meanBy from "lodash/meanBy";
import moment from "moment";

Vue.use(Vuex);

const nonNumericColumns = new Set(["tag", "name"]);

const state = {
  tag: null,
  loading: true,
  clan: window.__CLAN__ || [],
  previousData: window.__CLAN__ || [],
  lastUpdated: window.__LAST_UPDATED__ || "",
  days: 7,
  similarClansAvg: {},
  daysSpan: 7,
  sortField: "value",
  apiError: null
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
  },
  setApiError(state, field) {
    state.apiError = field;
  }
};

async function handleResponse(promise, commit, success, error = "setApiError") {
  const response = await promise;
  if (response.status == 200) {
    const data = await response.json();
    commit(success, data);
  } else {
    const e = await response.json();
    e.status = response.status;
    console.warn(
      `Error while fetch data from API. Status: ${e.status}, Message: ${
        e.error
      }`
    );
    commit(error, e);
  }
}

const actions = {
  async fetchClanData({ commit, dispatch, getters: { path } }) {
    const nowPromise = fetch(`${path}.json`);
    const previousPromise = fetch(`${path}.json?daysAgo=${state.days}`);
    commit("stopLoading");
    await handleResponse(previousPromise, commit, "setPreviousData");
    await handleResponse(nowPromise, commit, "setClan");

    dispatch("fetchSimilarClansStats");
  },
  async fetchSimilarClansStats({ commit, getters: { path } }) {
    const similarClansPromise = await fetch(`${path}/similar/avg.json`);
    await handleResponse(similarClansPromise, commit, "setSimilarClansAvg");
  },
  async loadDaysAgo(
    {
      commit,
      getters: { path }
    },
    days
  ) {
    commit("setDays", days);
    commit("startLoading");
    const promise = await fetch(`${path}.json?daysAgo=${days}`);
    await handleResponse(promise, commit, "setPreviousData");
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
        numeric: !nonNumericColumns.has(camelCase(column))
      }));
    } else {
      return [];
    }
  },
  path({ tag }) {
    return `/clan/${tag.replace("#", "")}`;
  },
  lastUpdatedAgo({ lastUpdated }) {
    return moment(lastUpdated).fromNow();
  },
  clanAverage(state, { tableData }) {
    const a = c => meanBy(tableData, c + ".delta");
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
            previousRow && !nonNumericColumns.has(column)
              ? value - previousRow[column]
              : 0;
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

export default new Vuex.Store({
  strict: true,
  state,
  getters,
  actions,
  mutations
});
