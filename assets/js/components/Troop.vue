<template>
  <b-tooltip :label="name" position="is-right" type="is-dark" active="showTooltip" delay="350">
    <div class="troop" :class="name | iconClass">
      <slot></slot>
    </div>
  </b-tooltip>
</template>

<script>
import kebabCase from "lodash/kebabCase";

export default {
  props: {
    name: String,
    showTooltip: {
      type: Boolean,
      default: true,
    },
  },
  filters: {
    iconClass(value) {
      return kebabCase(value);
    },
  },
};
</script>

<style lang="scss" scoped>
.troop {
  display: inline-block;
  border-radius: 4px;
  box-shadow: 0 0 0 1px #eee;
}
</style>
