<template>
  <ol class="columns is-multiline is-gapless">
    <li v-for="player in players" :key="player.tag" class="column is-4">
      <a href="#" @click="pickPlayer(player)">
        <span class="trophies is-pulled-right"> <i class="fa fa-trophy" aria-hidden="true"></i> {{ player.trophies.toLocaleString() }} </span>
        <span class="name has-text-weight-semibold">{{ player.name }}</span> <br />
        <small class="player-tag is-size-7 has-text-weight-light">{{ player.tag }}</small>
      </a>
    </li>
  </ol>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: ["players"],
  data() {
    return {
      selectedPlayer: Object,
    };
  },
  methods: {
    pickPlayer(player) {
      this.selectedPlayer = player;
      this.$emit("update:selectedPlayer", player);
    },
  },
  computed: {
    ...mapState(["foundClan", "savedTag"]),
  },
};
</script>
<style lang="scss" scoped>
a {
  border: 1px solid #eee;
  display: block;
  padding: 0.5em;
  margin: 0.2em;

  &:hover {
    background-color: #eee;
  }
}
</style>
