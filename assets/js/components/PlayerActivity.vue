<template>
  <div class="container">
    <b-tabs size="is-medium" @change="onChange">
      <b-tab-item label="Attacks">
        <activity-distribution ref="attacks" name="attack_wins"></activity-distribution>
      </b-tab-item>

      <b-tab-item label="Donations">
        <activity-distribution ref="donations" name="donations"></activity-distribution>
      </b-tab-item>

      <b-tab-item label="Trophies">
        <activity-distribution ref="trophies" name="trophies"></activity-distribution>
      </b-tab-item>
      <b-tab-item label="DE Grab">
        <activity-distribution ref="loot" name="de_grab"></activity-distribution>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import ActivityDistribution from "./ActivityDistribution";
import { mapActions, mapState } from "vuex";

export default {
  components: {
    ActivityDistribution
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
