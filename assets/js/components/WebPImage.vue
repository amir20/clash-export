<template>
  <picture>
    <source :srcset="`/static/images/${name}.webp`" type="image/webp" />
    <source :srcset="`/static/images/${name}.png`" type="image/png" />
    <img :src="`/static/images/${name}.png`" :width="width" :height="height" />
  </picture>
</template>

<script>
export default {
  props: ["name", "width", "height"],
};
</script>
