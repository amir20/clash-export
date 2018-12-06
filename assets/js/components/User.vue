<template>
  <b-dropdown position="is-bottom-left">
    <a class="navbar-item button is-transparent" slot="trigger">
      <b-icon pack="fas" icon="user" size="is-small" class="user"></b-icon>
      <span>{{ profile.name }}</span>
      <b-icon pack="fas" icon="angle-down" size="is-small"></b-icon>
    </a>

    <b-dropdown-item has-link> <a href="/updates">Your clan</a> </b-dropdown-item>
    <b-dropdown-item has-link> <a href="/updates">Player Page</a> </b-dropdown-item>
    <b-dropdown-item separator></b-dropdown-item>
    <b-dropdown-item has-link> <a href="/updates">Forget Me</a> </b-dropdown-item>
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
    return { profile: store.get(PLAYER_KEY) };
  },
  methods: {}
};
</script>
