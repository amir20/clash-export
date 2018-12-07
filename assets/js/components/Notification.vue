<template></template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState(["daysSpan"])
  },
  mounted() {
    if (this.daysSpan < 3) {
      this.$snackbar.open({
        message:
          "Hey stranger! This is the first time I am seeing your clan. It will take a few days to collect historical data. Come back again to see your clan's activity.",
        type: "is-warning",
        position: "is-bottom-left",
        actionText: "Got it",
        duration: 20000
      });
    }
  }
};
</script>
