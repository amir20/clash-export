<template>
  <div class="container" v-if="showInsights">
    <h3 class="title is-4 is-marginless">Troops progress for town hall {{ insights.th_level }}</h3>

    <div class="columns is-vcentered">
      <div class="column">
        <progress class="progress is-success is-large" :value="Math.ceil(insights.th_ratio * 100)" max="100">{{
          Math.ceil(insights.th_ratio * 100)
        }}</progress>
      </div>
      <div class="column is-narrow is-size-2">{{ Math.ceil(insights.th_ratio * 100) }}%</div>
    </div>

    <h3 class="title is-4 is-marginless">Troops progress for builder hall {{ insights.bh_level }}</h3>
    <div class="columns is-vcentered">
      <div class="column">
        <progress class="progress is-warning is-large" :value="Math.ceil(insights.bh_ratio * 100)" max="100">{{
          Math.ceil(insights.bh_ratio * 100)
        }}</progress>
      </div>
      <div class="column is-narrow is-size-2">{{ Math.ceil(insights.bh_ratio * 100) }}%</div>
    </div>

    <h3 class="title is-4 is-marginless">Recommended Upgrades</h3>
    <div class="columns is-vcentered">
      <div class="column is-6">
        You should upgrade the following items based off similar players that are the same level as you.
      </div>
      <div class="column is-6">
        <troop
          v-if="homeBaseTroop"
          :name="homeBaseTroop.name"
          class="is-tooltip-right tooltip"
          :data-tooltip="homeBaseTroop.name"
        ></troop>
        <troop
          v-if="builderBaseTroop"
          :name="builderBaseTroop.name"
          class="is-tooltip-right tooltip"
          :data-tooltip="homeBaseTroop.name"
        ></troop>
      </div>
    </div>
  </div>
  <div class="container" v-else>
    Insights are recommendations that are shown on your own profile. This information is only available to you once you
    signin as yourself and claim your profile.

    <br />
    <br />

    <div class="is-secret">
      <h3 class="title is-4 is-marginless">Troops progress for town hall {{ insights.th_level }}</h3>
      <div class="columns is-vcentered">
        <div class="column"><progress class="progress is-success is-large" :value="88" max="100">--%</progress></div>
        <div class="column is-narrow is-size-2">--%</div>
      </div>

      <h3 class="title is-4 is-marginless">Troops progress for builder hall {{ insights.bh_level }}</h3>
      <div class="columns is-vcentered">
        <div class="column"><progress class="progress is-warning is-large" :value="55" max="100"></progress></div>
        <div class="column is-narrow is-size-2">--%</div>
      </div>
    </div>
  </div>
</template>

<script>
import store from "store/dist/store.modern";
import Troop from "./Troop";
import maxBy from "lodash/maxBy";

const PLAYER_KEY = "savedPlayer";
export default {
  props: ["insights", "playerTag"],
  components: {
    Troop
  },
  data() {
    return { savedPlayer: store.get(PLAYER_KEY) };
  },
  computed: {
    homeBaseTroop() {
      return maxBy(this.insights.home, i => i.delta);
    },
    builderBaseTroop() {
      return maxBy(this.insights.builderBase, i => i.delta);
    },
    showInsights() {
      return this.playerTag == this.savedPlayer.tag;
    }
  }
};
</script>

<style scoped>
.is-secret {
  filter: grayscale(100%) blur(5px);
}
</style>
