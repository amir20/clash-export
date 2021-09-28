<template>
  <div class="columns is-mobile is-centered-mobile" v-if="loading">
    <div class="column is-narrow">
      <div class="lds-ring mr-1 has-text-right">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    <div class="column is-narrow">
      <span class="loading">updating</span>
    </div>
  </div>
  <time v-else>Updated {{ text }}</time>
</template>

<script>
import { mapState } from "vuex";
import formatDistance from "date-fns/formatDistance";

export default {
  data() {
    return {
      text: "",
      interval: null,
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
    },
  },
  methods: {
    updateFromNow() {
      this.text = formatDistance(this.lastUpdated, new Date(), {
        addSuffix: true,
      });
    },
  },
  watch: {
    lastUpdated() {
      this.updateFromNow();
    },
  },
};
</script>

<style scoped lang="scss">
@media screen and (max-width: 769px) {
  .is-centered-mobile {
    justify-content: center;
  }
}

.loading {
  text-align: left;
  width: 80px;
  display: inline-block;
  &:after {
    display: inline-block;
    animation: dotty steps(1, end) 2s infinite;
    content: "";
  }
}

@keyframes dotty {
  0% {
    content: "";
  }
  25% {
    content: ".";
  }
  50% {
    content: "..";
  }
  75% {
    content: "...";
  }
  100% {
    content: "";
  }
}

.lds-ring div {
  box-sizing: border-box;
  display: block;
  position: absolute;
  width: 14px;
  height: 14px;
  margin: 7px;
  border: 1px solid #444;
  border-radius: 50%;
  animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  border-color: #444 transparent transparent transparent;
}

.lds-ring div:nth-child(1) {
  animation-delay: -0.45s;
}

.lds-ring div:nth-child(2) {
  animation-delay: -0.3s;
}

.lds-ring div:nth-child(3) {
  animation-delay: -0.15s;
}

@keyframes lds-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
