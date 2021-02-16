<template>
  <b-tooltip :label="label" position="is-right" :type="isSuccess ? 'is-success' : 'is-dark'" :active="hasPermission" :delay="100" :always="forceTooltip">
    <span class="tag is-light" @click="writeToClipboard($event)" :class="{ enabled: hasPermission }">
      <i class="fas fa-hashtag mr-1"></i>
      {{ value.substr(1) }}
    </span>
  </b-tooltip>
</template>

<script>
export default {
  props: {
    value: { type: String },
  },
  data() {
    return {
      label: "Copy",
      hasPermission: false,
      forceTooltip: false,
      isSuccess: false,
    };
  },
  async created() {
    const result = await navigator.permissions.query({ name: "clipboard-write" });
    this.hasPermission = result.state == "granted" || result.state == "prompt";
  },
  methods: {
    async writeToClipboard(e) {
      e.preventDefault();
      if (this.hasPermission) {
        await navigator.clipboard.writeText(this.value);
        this.forceTooltip = true;
        this.label = "Copied!";
        this.isSuccess = true;
        setTimeout(() => {
          this.forceTooltip = false;
          setTimeout(() => {
            this.label = "Copy";
            this.isSuccess = false;
          }, 1000);
        }, 2500);
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.tag.enabled {
  cursor: pointer;
}
</style>
