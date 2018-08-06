import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const STORAGE_KEY = "lastTag";

const state = {
  foundClan: null,
  savedTag: localStorage ? localStorage.getItem(STORAGE_KEY) : null
};

const mutations = {
  setFoundClan(state, clan) {
    state.foundClan = clan;
  },
  setSavedTag(state, tag) {
    state.savedTag = tag;
    try {
      if (tag == null) {
        localStorage.removeItem(STORAGE_KEY);
      } else {
        localStorage.setItem(STORAGE_KEY, tag);
      }
    } catch (e) {
      // Do nothing as some browsers block this in private mode
    }
  },
  clearSavedTag(state) {
    state.savedTag = null;
    state.foundClan = null;
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (error) {}
  }
};

const actions = {};

// getters are functions
const getters = {};

export default new Vuex.Store({
  strict: true,
  state,
  getters,
  actions,
  mutations
});
