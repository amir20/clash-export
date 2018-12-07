<template>
  <b-dropdown position="is-bottom-left" v-if="savedPlayer">
    <a class="navbar-item button is-transparent" slot="trigger">
      <b-icon pack="fas" icon="user" size="is-small" class="user"></b-icon>
      <span>{{ savedPlayer.name }}</span>
      <b-icon pack="fas" icon="angle-down" size="is-small"></b-icon>
    </a>
    <template v-if="user">
      <b-dropdown-item has-link>
        <a :href="`/clan/${user.clan.slug}`">{{ user.clan.name }}</a>
      </b-dropdown-item>
      <b-dropdown-item has-link> <a :href="`/player/${user.slug}`">Your profile</a> </b-dropdown-item>
      <b-dropdown-item separator></b-dropdown-item>
      <b-dropdown-item has-link> <a @click="removeUser">Forget Me</a> </b-dropdown-item>
    </template>
  </b-dropdown>
</template>

<style scoped>
.button.is-transparent {
  background: transparent;
  border-color: transparent;
}
</style>
<script>
import store from "store/dist/store.modern";
const PLAYER_KEY = "savedPlayer";

export default {
  data() {
    return { savedPlayer: store.get(PLAYER_KEY), user: null };
  },
  async created() {
    this.fetchUser();
  },
  mounted() {
    document.addEventListener("user-signin", e => {
      this.savedPlayer = store.get(PLAYER_KEY);
      this.fetchUser();
    });
  },
  methods: {
    removeUser() {
      store.remove(PLAYER_KEY);
      this.savedPlayer = null;
    },
    async fetchUser() {
      if (this.savedPlayer) {
        this.user = await (await fetch(`/player/${this.savedPlayer.tag.replace("#", "")}.json`)).json();
      }
    }
  }
};
</script>
