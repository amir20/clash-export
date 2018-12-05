<template>
  <ul>
    <li v-for="player in players" :key="player.Tag">
      <a href="">
        {{ player.Name }} <small>{{ player.Tag }}</small>
      </a>
    </li>
  </ul>
</template>

<script>
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";

export default {
  props: ["players"],
  data() {
    return {
      selectedPlayer: Object
    };
  },
  computed: {
    ...mapState(["foundClan", "savedTag"])
  }
};
</script>
<style scoped>
a[disabled="disabled"] {
  pointer-events: none;
}
</style>
