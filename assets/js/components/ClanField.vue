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
  created() {
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
      function animate(time) {
        requestAnimationFrame(animate);
        TWEEN.update(time);
      }
      requestAnimationFrame(animate);
      new TWEEN.Tween({ tweeningValue: startValue })
        .to({ tweeningValue: endValue }, 2500)
        .onUpdate(({ tweeningValue }) => (this.tweeningValue = Math.ceil(tweeningValue)))
        .start();
      animate();
    }
  }
};
</script>
