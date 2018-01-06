<template>
<ul>
    <li :class="{'is-active': days === 1}">
        <a @click="changeDays(1)">Yesterday</a>
    </li>
    <li :class="{'is-active': days === 7}">
        <a @click="changeDays(7)">This Week</a>
    </li>
    <li :class="{'is-active': days ===30}">
        <a @click="changeDays(30)">Last Month</a>
    </li>
</ul>
</template>

<script>
export default {
  data() {
    return {
      days: 7
    };
  },
  created() {
    this.$bus.$on("days-changed-event", days => {
      this.days = days;
    });
  },
  methods: {
    changeDays(days) {
      this.$bus.$emit("days-changed-event", days);
    }
  }
};
</script>
