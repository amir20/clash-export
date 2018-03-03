import Vue from 'vue'
import Vuex from 'vuex'
import camelCase from "lodash/camelCase";
import reduce from "lodash/reduce";
import keyBy from "lodash/keyBy";
import isNumber from "lodash/isNumber";

Vue.use(Vuex);


const state = {
    tag: null,
    loading: true,
    clan: null,
    previousData: null,
    days: 7,
    similarClansAvg: null
}


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
    setSimilarClans(state, similarClans) {
        state.similarClans = similarClans;
    },
    startLoading(state) {
        state.loading = true;
    },
    stopLoading(state) {
        state.loading = false;
    }
}

const actions = {
    async fetchClanData({ commit, getters: { path } }, clusterLabel) {
        const nowPromise = fetch(`${path}.json`);
        const previousPromise = fetch(`${path}.json?daysAgo=${state.days}`);
        commit('stopLoading');

        const previousData = await (await previousPromise).json();
        commit('setPreviousData', previousData);

        const clan = await (await nowPromise).json();
        commit('setClan', clan);

        const similarClansAvg = await (await fetch(`/similar-clans/${clusterLabel}/avg.json`)).json();
        commit('setSimilarClans', similarClansAvg);
    },
    async loadDaysAgo({ commit, getters: { path } }, days) {
        commit('setDays', days);
        commit('startLoading');
        const data = await fetch(`${path}.json?daysAgo=${days}`);
        const previousData = await data.json();
        commit('setPreviousData', previousData);
        commit('stopLoading');
    },
}

// getters are functions
const getters = {
    header({ clan }) {
        return clan[0].map((column, index) => ({
            label: column,
            field: camelCase(column),
            numeric: index > 1
        }));
    },
    path({ tag }) {
        return `/clan/${tag.replace("#", "")}`;
    },
    tableData(state, getters) {
        const data = convertToMap(getters.header, state.clan.slice(1));
        const previousData = convertToMap(getters.header, state.previousData.slice(1));
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
}

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
}


export default new Vuex.Store({
    strict: true,
    state,
    getters,
    actions,
    mutations
})
