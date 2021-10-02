<template>
  <div class="container" v-if="loading || hasData">
    <b-tabs size="is-medium" @input="onChange">
      <b-tab-item label="Attacks" value="attacks">
        <activity-distribution
          ref="attacks"
          :labels="playerActivity.labels"
          :user-series="user.attackWins"
          :player-series="playerActivity.attackWins"
          :loading="loading"
          :show-user="hasDifferentUser"
        >
        </activity-distribution>
      </b-tab-item>
      <b-tab-item label="Donations" value="donations">
        <activity-distribution
          ref="donations"
          :labels="playerActivity.labels"
          :user-series="user.donations"
          :player-series="playerActivity.donations"
          :loading="loading"
          :show-user="hasDifferentUser"
        >
        </activity-distribution>
      </b-tab-item>

      <b-tab-item label="Trophies" value="trophies">
        <activity-distribution
          ref="trophies"
          :labels="playerActivity.labels"
          :user-series="user.trophies"
          :player-series="playerActivity.trophies"
          :loading="loading"
          :show-user="hasDifferentUser"
        >
        </activity-distribution>
      </b-tab-item>
      <b-tab-item label="DE Grab" value="loot">
        <activity-distribution
          ref="loot"
          :labels="playerActivity.labels"
          :user-series="user.deGrab"
          :player-series="playerActivity.deGrab"
          :loading="loading"
          :show-user="hasDifferentUser"
        >
        </activity-distribution>
      </b-tab-item>
    </b-tabs>
  </div>
  <div class="container" v-else>
    <div v-if="isSameUser">Chief! Come back tomorrow. I am still collecting data to be able to show your activity.</div>
    <div v-else>This player doesn't have any activity yet. Try again tomorrow after there is a chance to collect some data.</div>
  </div>
</template>

<script>
import ActivityDistribution from "./ActivityDistribution";
import times from "lodash/times";
import UserMixin from "../user";
import { request } from "../client";
import { gql } from "graphql-request";

export default {
  components: {
    ActivityDistribution,
  },
  mixins: [UserMixin],
  props: ["tag"],
  data() {
    return {
      loading: true,
      playerActivity: {},
      user: {
        attackWins: [],
        donations: [],
        deGrab: [],
        trophies: [],
      },
    };
  },
  async created() {
    this.loading = true;
    const data = await request(
      gql`
        query GetPlayerActivities($playerTag: String!, $userTag: String = "", $hasUser: Boolean!) {
          player: player(tag: $playerTag) {
            tag
            activity {
              labels
              attackWins
              donations
              deGrab
              trophies
            }
          }
          user: player(tag: $userTag) @include(if: $hasUser) {
            tag
            activity {
              labels
              attackWins
              donations
              deGrab
              trophies
            }
          }
        }
      `,
      {
        playerTag: this.tag,
        userTag: this.userTag,
        hasUser: this.hasDifferentUser,
      }
    );

    const { user, player } = data;
    this.playerActivity = player.activity;
    if (user) {
      this.user = user.activity;
      if (user.activity.labels.length < this.playerActivity.labels.length) {
        const zeros = this.playerActivity.labels.length - user.activity.labels.length;
        const nulls = times(zeros, null);
        this.user.attackWins.unshift(...nulls);
        this.user.donations.unshift(...nulls);
        this.user.trophies.unshift(...nulls);
        this.user.deGrab.unshift(...nulls);
      } else if (user.activity.labels.length > this.playerActivity.labels.length) {
        const length = this.playerActivity.labels.length;
        this.user.attackWins = this.user.attackWins.slice(-length);
        this.user.donations = this.user.donations.slice(-length);
        this.user.trophies = this.user.trophies.slice(-length);
        this.user.deGrab = this.user.deGrab.slice(-length);
      }
    }
    this.loading = false;
  },
  methods: {
    onChange(tab) {
      const chart = this.$refs[tab];
      setTimeout(() => chart.redraw(), 100);
    },
  },
  computed: {
    hasDifferentUser() {
      return this.hasUser && this.userTag !== this.tag;
    },
    isSameUser() {
      return this.hasUser && this.userTag === this.tag;
    },
    hasData() {
      return this.playerActivity.labels.length > 0;
    },
  },
};
</script>

<style lang="scss" scoped>
@media screen and (max-width: 769px) {
  /deep/ .b-tabs .tab-content {
    padding-left: 0;
    padding-right: 0;
    margin-left: -1em;
    margin-right: -1em;
  }
}
</style>
