<template>
<b-dropdown v-model="days" @change="changeDays">
        <button class="button is-success" type="button" slot="trigger">
            <template v-if="days == 1">
                <b-icon icon="calendar-alt" size="is-small"></b-icon>
                <span>Yesterday</span>
            </template>
            <template v-else-if="days == 7">
                <b-icon icon="calendar-alt" size="is-small"></b-icon>
                <span>Last Week</span>
            </template>
            <template v-else-if="days == 30">
                <b-icon icon="calendar-alt" size="is-small"></b-icon>
                <span>Last Month</span>
            </template>
            <b-icon icon="chevron-down" size="is-small"></b-icon>
        </button>

        <b-dropdown-item :value="1">
            <div class="media">
                <b-icon class="media-left" icon="clock"></b-icon>
                <div class="media-content">
                    <h3>Yesterday</h3>
                    <small>Compare your data to yesterday</small>
                </div>
            </div>
        </b-dropdown-item>

        <b-dropdown-item :value="7">
            <div class="media">
                <b-icon class="media-left" icon="clock"></b-icon>
                <div class="media-content">
                    <h3>Last Week</h3>
                    <small>Compare your data to a week ago</small>
                </div>
            </div>
        </b-dropdown-item>
        <b-dropdown-item :value="30">
            <div class="media">
                <b-icon class="media-left" icon="clock"></b-icon>
                <div class="media-content">
                    <h3>Last Month</h3>
                    <small>Compare your data to last month</small>
                </div>
            </div>
        </b-dropdown-item>
    </b-dropdown>
</template>

<script>
export default {
  data() {
    return {
      days: 7,
      totalDays: 30
    };
  },
  created() {
    this.$bus.$on("days-changed-event", days => {
      this.days = days;
    });
    this.$bus.$on("days-of-data", totalDays => {
      this.totalDays = totalDays;
    });
  },
  methods: {
    changeDays(days) {
      this.$bus.$emit("days-changed-event", days);
    }
  }
};
</script>
