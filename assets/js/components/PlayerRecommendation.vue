<template>
  <div class="container" v-if="showInsights">
    <h3 class="title is-4 is-marginless">Troops progress for town hall {{ insights.th_level }}</h3>

    <div class="columns is-vcentered">
      <div class="column">
        <progress class="progress is-success is-large" :value="Math.ceil(insights.th_ratio * 100)" max="100">
          {{ Math.ceil(insights.th_ratio * 100) }}
        </progress>
      </div>
      <div class="column is-narrow is-size-2">{{ Math.ceil(insights.th_ratio * 100) }}%</div>
    </div>

    <h3 class="title is-4 is-marginless">Troops progress for builder hall {{ insights.bh_level }}</h3>
    <div class="columns is-vcentered">
      <div class="column">
        <progress class="progress is-warning is-large" :value="Math.ceil(insights.bh_ratio * 100)" max="100">
          {{ Math.ceil(insights.bh_ratio * 100) }}
        </progress>
      </div>
      <div class="column is-narrow is-size-2">{{ Math.ceil(insights.bh_ratio * 100) }}%</div>
    </div>
    <div class="columns">
      <div class="column">
        <h3 class="title is-4 is-marginless">Recommended Upgrades</h3>
        <div class="columns is-vcentered">
          <div class="column is-8">
            You should upgrade the following items based on similar players same level as you. This recommendation may change as other players upgrade different
            troops.
          </div>
          <div class="column">
            <troop v-if="homeBaseTroop" :name="homeBaseTroop.name" class="is-tooltip-right tooltip" :data-tooltip="homeBaseTroop.name"></troop>
            <troop v-if="builderBaseTroop" :name="builderBaseTroop.name" class="is-tooltip-right tooltip" :data-tooltip="builderBaseTroop.name"></troop>
            <b v-if="!homeBaseTroop && !builderBaseTroop">No recommendations right now. Great job!</b>
          </div>
        </div>
      </div>
      <div class="column is-narrow is-hidden-mobile"><web-p-image name="builder-show" width="280" /></div>
    </div>
  </div>
  <div class="container" v-else>
    <div class="columns">
      <div class="column">
        Insights are recommendations that are shown on your own profile. This information is only available to you after you signin and claim your profile. Go
        to home page and select your player profile after you have found your clan.
      </div>
      <div class="column is-narrow is-hidden-mobile"><web-p-image name="builder-show" width="300" /></div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import maxBy from "lodash/maxBy";
import Troop from "./Troop";
import WebPImage from "./WebPImage";
import UserMixin from "../user";

export default {
  props: [],
  mixins: [UserMixin],
  components: {
    Troop,
    WebPImage,
  },
  computed: {
    ...mapState(["player"]),
    homeBaseTroop() {
      return maxBy(this.player.insights.home, (i) => i.delta);
    },
    builderBaseTroop() {
      return maxBy(this.player.insights.builderBase, (i) => i.delta);
    },
    showInsights() {
      return this.player.tag === this.userTag;
    },
    insights() {
      return this.player.insights;
    },
  },
};
</script>

<style lang="scss" scoped></style>
