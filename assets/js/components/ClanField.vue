<template>
  <span v-if="tweeningValue != null" :class="{ [positiveClass]: tweeningValue > 0, [negativeClass]: tweeningValue < 0 }">
    <template v-if="showPlusSign && tweeningValue > 0">+</template>{{ tweeningValue.toLocaleString(undefined, localeStyle) }}
  </span>
</template>

<script>
import TWEEN from "@tweenjs/tween.js";

export default {
  props: {
    value: { type: Number },
    showPlusSign: { type: Boolean, default: false },
    positiveClass: { type: String, default: "" },
    negativeClass: { type: String, default: "" },
    localeStyle: { type: Object, default: () => {} },
  },
  data: function () {
    return {
      tweeningValue: 0,
    };
  },
  created() {
    this.tweeningValue = this.value;
  },
  watch: {
    value(newValue, oldValue) {
      this.tween(this.tweeningValue, this.value);
    },
  },
  methods: {
    tween(startValue, endValue) {
      function animate(time) {
        requestAnimationFrame(animate);
        TWEEN.update(time);
      }
      new TWEEN.Tween({ tweeningValue: startValue })
        .to({ tweeningValue: endValue }, 1200)
        .delay(Math.random() * 800)
        .easing(TWEEN.Easing.Quadratic.Out)
        .onUpdate(({ tweeningValue }) => (this.tweeningValue = this.tweeningValue > 1 ? Math.ceil(tweeningValue) : tweeningValue))
        .start();
      animate();
    },
  },
};
</script>
