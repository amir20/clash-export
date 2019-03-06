<template>
  <div class="container">
    <b-tabs size="is-medium" @change="onChange">
      <b-tab-item label="Attacks">
        <activity-distribution
          ref="attacks"
          :labels="player.labels"
          :user-series="user.attackWins"
          :player-series="player.attackWins"
          :loading="loading"
          :show-user="hasDifferentUser"
        >
        </activity-distribution>
      </b-tab-item>

      <b-tab-item label="Donations">
        <activity-distribution
          ref="donations"
          :labels="player.labels"
          :user-series="user.donations"
          :player-series="player.donations"
          :loading="loading"
          :show-user="hasDifferentUser"
        >
        </activity-distribution>
      </b-tab-item>

      <b-tab-item label="Trophies">
        <activity-distribution
          ref="trophies"
          :labels="player.labels"
          :user-series="user.trophies"
          :player-series="player.trophies"
          :loading="loading"
          :show-user="hasDifferentUser"
        >
        </activity-distribution>
      </b-tab-item>
      <b-tab-item label="DE Grab">
        <activity-distribution
          ref="loot"
          :labels="player.labels"
          :user-series="user.deGrab"
          :player-series="player.deGrab"
          :loading="loading"
          :show-user="hasDifferentUser"
        >
        </activity-distribution>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import ActivityDistribution from "./ActivityDistribution";
import times from "lodash/times";
import UserMixin from "../user";
import { apolloClient } from "../client";
import { gql } from "apollo-boost";

export default {
  components: {
    ActivityDistribution
  },
  mixins: [UserMixin],
  props: ["playerTag"],
  data() {
    return {
      loading: true,
      player: {},
      user: {
        attackWins: [],
        donations: [],
        deGrab: [],
        trophies: []
      }
    };
  },
  async created() {
    this.loading = true;
    const { data } = await apolloClient.query({
      query: gql`
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
      variables: {
        playerTag: this.playerTag,
        userTag: this.userTag,
        hasUser: this.hasDifferentUser
      }
    });

    const { user, player } = data;
    this.player = player.activity;
    if (user) {
      this.user = user.activity;
      if (user.activity.labels.length < player.activity.labels.length) {
        const zeros = player.activity.labels.length - user.activity.labels.length;
        const nulls = times(zeros, null);
        this.user.attackWins.unshift(...nulls);
        this.user.donations.unshift(...nulls);
        this.user.trophies.unshift(...nulls);
        this.user.deGrab.unshift(...nulls);
      } else if (user.activity.labels.length > player.activity.labels.length) {
        const length = player.activity.labels.length;
        this.user.attackWins = this.user.attackWins.slice(-length);
        this.user.donations = this.user.donations.slice(-length);
        this.user.trophies = this.user.trophies.slice(-length);
        this.user.deGrab = this.user.deGrab.slice(-length);
      }
    }
    this.loading = false;
  },
  methods: {
    onChange(index) {
      const { attacks, donations, trophies, loot } = this.$refs;
      const chart = [attacks, donations, trophies, loot][index];
      setTimeout(() => chart.redraw(), 100);
    }
  },
  computed: {
    hasDifferentUser() {
      return this.hasUser && this.userTag !== this.playerTag;
    }
  }
};
</script>

<style lang="scss" scoped></style>
