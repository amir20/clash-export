<template>
<div class="navbar-start">
    <div class="navbar-item">
        <b-dropdown v-model="days" @change="loadDaysAgo" hoverable>
            <button class="button is-info" type="button" slot="trigger" :key="days">
                <template v-if="days == 1">
                    <b-icon icon="hourglass" size="is-small" pack="far"></b-icon>
                    <span>Compare to Yesterday</span>
                </template>
                <template v-else-if="days == 7">
                    <b-icon icon="calendar-alt" size="is-small" pack="far"></b-icon>
                    <span>Compare to Last Week</span>
                </template>
                <template v-else-if="days == 30">
                    <b-icon icon="calendar" size="is-small" pack="far"></b-icon>
                    <span>Compare to Last Month</span>
                </template>
                <b-icon icon="chevron-down" size="is-small"></b-icon>
            </button>

            <b-dropdown-item :value="1" v-if="daysSpan > 0">
                <div class="media">
                    <b-icon class="media-left" icon="hourglass" pack="far"></b-icon>
                    <div class="media-content">
                        <h3>Yesterday</h3>
                        <small>Compare your data to yesterday</small>
                    </div>
                </div>
            </b-dropdown-item>
            <b-dropdown-item :value="7" v-if="daysSpan > 2">
                <div class="media">
                    <b-icon class="media-left" icon="calendar-alt" pack="far"></b-icon>
                    <div class="media-content">
                        <h3>Last Week</h3>
                        <small>Compare your data to a week ago</small>
                    </div>
                </div>
            </b-dropdown-item>
            <b-dropdown-item :value="30" v-if="daysSpan > 15">
                <div class="media">
                    <b-icon class="media-left" icon="calendar" pack="far"></b-icon>
                    <div class="media-content">
                        <h3>Last Month</h3>
                        <small>Compare your data to last month</small>
                    </div>
                </div>
            </b-dropdown-item>
        </b-dropdown>
    </div>
    <div class="navbar-item">
        <b-dropdown v-model="sort" @change="setSortField" hoverable>
            <button class="button is-info" type="button" slot="trigger" :key="sort">
                <template v-if="sort === 'delta'">
                    <b-icon icon="clock" size="is-small" pack="far"></b-icon>
                    <span>Sort by Stats Changed</span>
                </template>
                <template v-else>
                    <b-icon icon="chart-line" size="is-small"></b-icon>
                    <span>Sort by Most Recent</span>
                </template>
                <b-icon icon="chevron-down" size="is-small"></b-icon>
            </button>
            <b-dropdown-item value="value">
                <div class="media">
                    <b-icon class="media-left" icon="chart-line"></b-icon>
                    <div class="media-content">
                        <h3>Most Recent Stats</h3>
                        <small>Compare your data using more recent stats</small>
                    </div>
                </div>
            </b-dropdown-item>
            <b-dropdown-item value="delta">
                <div class="media">
                    <b-icon class="media-left" icon="clock" pack="far"></b-icon>
                    <div class="media-content">
                        <h3>Stats Changed</h3>
                        <small>Sort the columns using the delta between today and previous stats</small>
                    </div>
                </div>
            </b-dropdown-item>
        </b-dropdown>
    </div>
</div>
</template>

<script>
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";

export default {
  data() {
    return {
      days: 7,
      sort: "value"
    };
  },
  methods: {
    ...mapActions(["loadDaysAgo"]),
    ...mapMutations(["setSortField"])
  },
  computed: {
    ...mapState(["daysSpan", "softField"])
  }
};
</script>
