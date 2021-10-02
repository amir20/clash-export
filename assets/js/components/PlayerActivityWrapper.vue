<template>
  <player-activity :tag="player.tag"></player-activity>
</template>

<script>
import PlayerActivity from "./PlayerActivity.vue";
import { mapState } from "vuex";

export default {
  components: {
    PlayerActivity,
  },
  props: [],

  methods: {},
  computed: {
    ...mapState(["player"]),
  },
};
</script>

<style lang="scss" scoped></style>
