<template>
  <player-activity :tag="player.tag"></player-activity>
</template>

<script>
const PlayerActivity = () => import("./PlayerActivity.vue");
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
