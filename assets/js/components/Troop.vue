<template>
  <div :class="name | iconClass"><slot></slot></div>
</template>

<script>
import kebabCase from "lodash/kebabCase";

export default {
  props: ["name"],
  filters: {
    iconClass(value) {
      return "coc-sprite--" + kebabCase(value);
    }
  }
};
</script>
