<template>
  <div class="troop" :class="name | iconClass">
    <slot></slot>
  </div>
</template>

<script>
import kebabCase from "lodash/kebabCase";

export default {
  props: ["name"],
  filters: {
    iconClass(value) {
      return kebabCase(value);
    }
  }
};
</script>

<style lang="scss" scoped>
.troop {
  display: inline-block;
  border-radius: 4px;
  border: 1px solid #eee;
}
</style>
