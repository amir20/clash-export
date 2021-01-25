import store from "store/dist/store.modern";
import { apolloClient } from "../client";
import { gql } from "@apollo/client/core";

const PLAYER_KEY = "savedPlayer";

export function saveUser(data) {
  store.set(PLAYER_KEY, data);
  document.dispatchEvent(new Event("user-state-changed"));
}

export function removeUser() {
  store.remove(PLAYER_KEY);
  document.dispatchEvent(new Event("user-state-changed"));
}

export function hasUser() {
  return store.get(PLAYER_KEY) != null;
}

export function userTag() {
  return hasUser() ? store.get(PLAYER_KEY).tag : null;
}

export default {
  data() {
    return {
      savedUser: store.get(PLAYER_KEY),
      userData: null,
    };
  },
  created() {
    this.fetchUser();
  },
  mounted() {
    document.addEventListener("user-state-changed", (e) => {
      this.savedUser = store.get(PLAYER_KEY);
      this.fetchUser();
    });
  },
  beforeDestroy() {
    document.removeEventListener("user-state-changed");
  },
  methods: {
    async fetchUser() {
      if (this.savedUser) {
        if (!window.userPromise) {
          window.userPromise = this.userPromise();
        }
        this.userData = await window.userPromise;
      }
    },
    async userPromise() {
      const { data } = await apolloClient.query({
        query: gql`
          query GetPlayerDetails($tag: String!) {
            player(tag: $tag) {
              name
              tag
              slug
              clan {
                slug
                tag
                name
              }
            }
          }
        `,
        variables: {
          tag: this.savedUser.tag,
        },
      });
      return data.player;
    },
    removeUser() {
      removeUser();
    },
    saveUser(data) {
      saveUser(data);
    },
  },
  computed: {
    userTag() {
      return this.hasUser ? this.savedUser.tag : null;
    },
    userName() {
      return this.hasUser ? this.savedUser.name : null;
    },
    hasUser() {
      return this.savedUser != null;
    },
    userSlug() {
      return this.userData ? this.userData.slug : null;
    },
  },
  watch: {
    savedUser(newValue) {
      if (newValue) {
        this.fetchUser();
      }
    },
  },
};
