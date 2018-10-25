<template>
   <div class="columns" v-if="player && player.troops">
     <div class="column is-6">
       <h4 class="title is-4 is-marginless">Troops</h4>
       <div v-for="troop in filterTroops(player.troops, 'home')" :key="troop.name + 'home'" :class="troop.name | iconClass">
         <small>{{ troop.level }}</small>
       </div>

       <h4 class="subtitle is-5 is-marginless">Builder Troops</h4>
       <div v-for="troop in filterTroops(player.troops, 'builderBase')" :key="troop.name + 'builder'" :class="troop.name | iconClass">
         <small>{{ troop.level }}</small>
       </div>
     </div>

     <div class="column is-3">
       <h4 class="title is-4 is-marginless">Spells</h4>
       <div v-for="spell in this.player.spells" :key="spell.name" :class="spell.name | iconClass">
         <small>{{ spell.level }}</small>
       </div>
     </div>
     <div class="column is-3">
       <h4 class="title is-4 is-marginless">Heros</h4>
       <div v-for="hero in filterTroops(player.heroes, 'home')" :key="hero.name" :class="hero.name | iconClass">
         <small>{{ hero.level }}</small>
       </div>
       <h4 class="subtitle is-5 is-marginless">Builder Base</h4>
       <div v-for="hero in filterTroops(player.heroes, 'builderBase')" :key="hero.name" :class="hero.name | iconClass">
         <small>{{ hero.level }}</small>
       </div>
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
  methods: {
    filterTroops(list, type) {
      return list.filter(troop => troop.village == type);
    }
  }
};
</script>

<style scoped>
[class*="coc-sprite--"] {
  margin: 1px;
  position: relative;

  small {
    font-size: 0.7em;
    position: absolute;
    right: 2px;
    bottom: 0;
    color: white;
    background: #333;
    padding: 0 1px;
    border-radius: 2px;
    min-width: 14px;
    text-align: center;
  }
}
</style>
