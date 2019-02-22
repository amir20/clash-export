<template>
  <div class="container">
    <b-tabs size="is-medium" @change="onChange">
      <b-tab-item label="Attacks">
        <attacks-distribution ref="attacks"></attacks-distribution>
      </b-tab-item>

      <b-tab-item label="Donations">
        <attacks-distribution ref="donations"></attacks-distribution>
      </b-tab-item>

      <b-tab-item label="Trophies">
        <attacks-distribution ref="trophies"></attacks-distribution>
      </b-tab-item>
      <b-tab-item label="Loot">
        <attacks-distribution ref="loot"></attacks-distribution>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import AttacksDistribution from "./AttacksDistribution";
import { mapActions, mapState } from "vuex";

export default {
  components: {
    AttacksDistribution
  },
  props: ["playerTag"],
  created() {
    this.fetchPlayer(this.playerTag);
  },
  computed: {
    ...mapState(["loading", "sortField", "similarClansAvg", "apiError", "playersStatus"])
  },
  methods: {
    ...mapActions(["fetchPlayer"]),
    onChange(index) {
      const { attacks, donations, trophies, loot } = this.$refs;
      const chart = [attacks, donations, trophies, loot][index];
      setTimeout(() => chart.redraw(), 100);
    }
  }
};
</script>

<style lang="scss" scoped></style>
