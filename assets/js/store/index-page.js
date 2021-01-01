import Vue from "vue";
import Vuex from "vuex";
import { event } from "../ga";
import store from "store/dist/store.modern";
import { saveUser, removeUser } from "../user";

Vue.use(Vuex);

const STORAGE_KEY = "lastTag";
const SKIP_PLAYER_QUESTION = "skipPlayerQuestion";

const state = {
  foundClan: null,
  savedTag: store.get(STORAGE_KEY),
  skipPlayerQuestion: store.get(SKIP_PLAYER_QUESTION) ? true : false,
};

const mutations = {
  setFoundClan(state, clan) {
    state.foundClan = clan;
  },
  setSavedPlayer(state, player) {
    event("saved-player", "Save Player");
    saveUser(player);
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
    state.skipPlayerQuestion = false;
    store.remove(STORAGE_KEY);
    store.remove(SKIP_PLAYER_QUESTION);
    removeUser();
  },
  doNotAskForPlayer(state) {
    event("skip-player", "Skip Player Saving");
    state.skipPlayerQuestion = true;
    store.set(SKIP_PLAYER_QUESTION, true);
  },
};

const actions = {};
const getters = {};

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});
