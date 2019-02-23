import Vue from "vue";
import Vuex from "vuex";
import { hasUser, userTag } from "../user";

Vue.use(Vuex);

const state = {
  playerTag: null,
  loggedUserActivity: {},
  playerActivity: {},
  hasLoggedUser: false,
  loading: true
};

const mutations = {
  setPlayerTag(state, tag) {
    state.playerTag = tag;
  },
  setLoggedUserActivity(state, data) {
    state.loggedUserActivity = data;
    state.hasLoggedUser = true;
  },
  setPlayerActivity(state, data) {
    state.playerActivity = data;
  },
  setLoading(state, data) {
    state.loading = data;
  }
};

const actions = {
  async fetchPlayer({ commit, dispatch }, playerTag) {
    commit("setPlayerTag", playerTag);
    if (hasUser() && userTag() !== playerTag) {
      const data = await (await fetch(`/player/${userTag().replace("#", "")}/activity.json`)).json();
      commit("setLoggedUserActivity", data);
    }
    const data = await (await fetch(`/player/${playerTag.replace("#", "")}/activity.json`)).json();
    commit("setPlayerActivity", data);
    commit("setLoading", false);
  }
};

const getters = {};
export default new Vuex.Store({
  strict: true,
  state,
  getters,
  actions,
  mutations
});
