<template>
  <span v-if="tweeningValue != null">{{ tweeningValue.toLocaleString() }}</span>
</template>

<script>
import { mapState } from "vuex";
import TWEEN from "@tweenjs/tween.js";

export default {
  props: ["initialValue", "name"],
  data: function() {
    return {
      tweeningValue: 0
    };
  },
  mounted: function() {
    this.tweeningValue = this.initialValue;
  },
  watch: {
    clanMeta(newValue, oldValue) {
      this.tween(this.initialValue, this.newValue);
    }
  },
  computed: {
    ...mapState(["clanMeta"]),
    newValue() {
      return this.name.split(".").reduce((prev, curr) => (prev ? prev[curr] : null), this.clanMeta);
    }
  },
  methods: {
    tween(startValue, endValue) {
      function animate() {
        if (TWEEN.update()) {
          requestAnimationFrame(animate);
        }
      }
      new TWEEN.Tween({ tweeningValue: startValue })
        .to({ tweeningValue: endValue }, 2500)
        .onUpdate(object => (this.tweeningValue = Math.ceil(object.tweeningValue)))
        .start();
      animate();
    }
  }
};
</script>
