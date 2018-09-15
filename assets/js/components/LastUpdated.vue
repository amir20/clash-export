<template>
    <time :datetime="lastUpdated.format()">Updated {{text}}</time>
</template>

<script>
import { mapState } from "vuex";
import formatDistance from "date-fns/formatDistance";

export default {
  data() {
    return {
      text: "",
      interval: null
    };
  },
  mounted() {
    this.updateFromNow();
    this.interval = setInterval(() => this.updateFromNow(), 30000);
  },
  destroyed() {
    clearInterval(this.interval);
  },
  computed: {
    ...mapState(["lastUpdated"])
  },
  methods: {
    updateFromNow() {
      this.text = formatDistance(this.lastUpdated, new Date(), {
        addSuffix: true
      });
    }
  },
  watch: {
    lastUpdated(newValue) {
      this.updateFromNow();
    }
  }
};
</script>
