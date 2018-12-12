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
            You should upgrade the following items based on similar players same level as you. This recommendation may
            change as other players upgrade different troops.
          </div>
          <div class="column">
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
              :data-tooltip="builderBaseTroop.name"
            ></troop>
          </div>
        </div>
      </div>
      <div class="column is-narrow is-hidden-mobile"><web-p-image name="builder-show" width="280" /></div>
    </div>
  </div>
  <div class="container" v-else>
    <div class="columns">
      <div class="column">
        Insights are recommendations that are shown on your own profile. This information is only available to you once
        you signin as yourself and claim your profile.
      </div>
      <div class="column is-narrow is-hidden-mobile"><web-p-image name="builder-show.png" width="300" /></div>
    </div>
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
import maxBy from "lodash/maxBy";
import Troop from "./Troop";
import WebPImage from "./WebPImage";
import UserMixin from "../user";

export default {
  props: ["insights", "playerTag"],
  mixins: [UserMixin],
  components: {
    Troop,
    WebPImage
  },
  computed: {
    homeBaseTroop() {
      return maxBy(this.insights.home, i => i.delta);
    },
    builderBaseTroop() {
      return maxBy(this.insights.builderBase, i => i.delta);
    },
    showInsights() {
      return this.playerTag == this.userTag;
    }
  }
};
</script>

<style scoped>
.is-secret {
  filter: grayscale(100%) blur(5px);
}
</style>
