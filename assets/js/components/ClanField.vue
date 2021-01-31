<template>
  <span v-if="tweeningValue != null" :class="{ [positiveClass]: tweeningValue > 0, [negativeClass]: tweeningValue < 0 }">
    <template v-if="showPlusSign && tweeningValue > 0">+</template>{{ tweeningValue.toLocaleString() }}
  </span>
</template>

<script>
import { mapState } from "vuex";
import TWEEN from "@tweenjs/tween.js";

export default {
  props: {
    name: { type: String },
    showPlusSign: { type: Boolean, default: false },
    positiveClass: { type: String, default: "" },
    negativeClass: { type: String, default: "" },
  },
  data: function () {
    return {
      tweeningValue: 0,
    };
  },
  created() {
    this.tweeningValue = this.targetValue;
  },
  watch: {
    targetValue(newValue, oldValue) {
      this.tween(this.tweeningValue, this.targetValue);
    },
  },
  computed: {
    ...mapState(["clan"]),
    targetValue() {
      return this.name.split(".").reduce((prev, curr) => (prev ? prev[curr] : null), this.clan);
    },
  },
  methods: {
    tween(startValue, endValue) {
      function animate(time) {
        requestAnimationFrame(animate);
        TWEEN.update(time);
      }
      requestAnimationFrame(animate);
      new TWEEN.Tween({ tweeningValue: startValue })
        .to({ tweeningValue: endValue }, 1200)
        .delay(Math.random() * 800)
        .easing(TWEEN.Easing.Quadratic.Out)
        .onUpdate(({ tweeningValue }) => (this.tweeningValue = Math.ceil(tweeningValue)))
        .start();
      animate();
    },
  },
};
</script>
