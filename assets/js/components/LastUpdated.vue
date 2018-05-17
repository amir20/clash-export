<template>
    <time :datetime="lastUpdated.format()">Updated {{text}}</time>
</template>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      text: "",
      interval: null
    };
  },
  mounted() {
    this.text = this.lastUpdated.fromNow();
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
      this.text = this.lastUpdated.fromNow();
    }
  },
  watch: {
    lastUpdated(newValue) {
      this.updateFromNow();
    }
  }
};
</script>
