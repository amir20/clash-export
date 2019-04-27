<template>
  <span v-if="loading">Updating...</span>
  <time v-else>Updated {{ text }}</time>
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
    ...mapState(["clan", "loading"]),
    lastUpdated() {
      return new Date(this.clan.updatedOn);
    }
  },
  methods: {
    updateFromNow() {
      this.text = formatDistance(this.lastUpdated, new Date(), {
        addSuffix: true
      });
    }
  },
  watch: {
    lastUpdated() {
      this.updateFromNow();
    }
  }
};
</script>
