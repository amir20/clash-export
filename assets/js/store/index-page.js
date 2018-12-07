import Vue from "vue";
import Vuex from "vuex";
import { event } from "../ga";
import store from "store/dist/store.modern";

Vue.use(Vuex);

const STORAGE_KEY = "lastTag";
const PLAYER_KEY = "savedPlayer";
const SKIP_PLAYER_QUESTION = "skipPlayerQuestion";

const state = {
  foundClan: null,
  savedTag: store.get(STORAGE_KEY),
  savedPlayer: store.get(PLAYER_KEY),
  skipPlayerQuestion: store.get(SKIP_PLAYER_QUESTION) ? true : false
};

const mutations = {
  setFoundClan(state, clan) {
    state.foundClan = clan;
  },
  setSavedPlayer(state, player) {
    event("saved-player", "Save Player");
    state.savedPlayer = player;
    store.set(PLAYER_KEY, player);
  },
  setSavedTag(state, tag) {
    event("saved-clan", "Save Clan");
    state.savedTag = tag;
    store.set(STORAGE_KEY, tag);
  },
  clearSavedTag(state) {
    event("saved-clan", "Reset Clan");
    state.savedTag = null;
    state.foundClan = null;
    state.savedPlayer = null;
    state.skipPlayerQuestion = false;
    store.remove(STORAGE_KEY);
    store.remove(PLAYER_KEY);
    store.remove(SKIP_PLAYER_QUESTION);
  },
  doNotAskForPlayer(state) {
    event("skip-player", "Skip Player Saving");
    state.savedPlayer = player;
    state.skipPlayerQuestion = true;
    store.set(SKIP_PLAYER_QUESTION, true);
  }
};

const actions = {};
const getters = {};

export default new Vuex.Store({
  strict: true,
  state,
  getters,
  actions,
  mutations
});
