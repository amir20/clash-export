<template>
   <div class="columns" v-if="player && player.troops">
     <div class="column is-6">
       <h4 class="title is-4">Troops</h4>
       <div v-for="troop in homeTroops" :key="troop.name" :class="troop.name | iconClass"></div>
     </div>

     <div class="column is-3">
       <h4 class="title is-4">Spells</h4>
       <div v-for="spell in this.player.spells" :key="spell.name" :class="spell.name | iconClass"></div>
     </div>
     <div class="column is-3">
       <h4 class="title is-4">Heros</h4>
       <div v-for="hero in this.player.heroes" :key="hero.name" :class="hero.name | iconClass"></div>
     </div>
   </div>
</template>

<script>
import kebabCase from "lodash/kebabCase";

export default {
  props: ["player"],
  data() {
    return {};
  },
  filters: {
    iconClass(value) {
      return "coc-sprite--" + kebabCase(value);
    }
  },
  computed: {
    homeTroops() {
      return this.player.troops.filter(troop => troop.village == "home");
    }
  }
};
</script>

<style scoped>
</style>
