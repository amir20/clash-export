<template>
</template>

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
          "Hey stranger! This is the first time I am seeing your clan and so it will take a while to collect historical data. Come back again in a few days to see your updated stats.",
        type: "is-warning",
        position: "is-bottom-left",
        actionText: "Got it",
        duration: 20000
      });
    }
  }
};
</script>
