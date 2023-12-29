<template>
  <div class="columns" v-if="player && player.troops">
    <div class="column is-6">
      <h4 class="title is-4 is-marginless">Troops</h4>
      <troop v-for="troop in filterTroops(player.troops, 'home')" :key="troop.name + 'home'" :name="troop.name">
        <small :class="{ max: troop.maxLevel == troop.level }">{{ troop.level }}</small>
      </troop>

      <h4 class="subtitle is-5 is-marginless">Builder Troops</h4>
      <troop v-for="troop in filterTroops(player.troops, 'builderBase')" :key="troop.name + 'builder'" :name="troop.name">
        <small :class="{ max: troop.maxLevel == troop.level }">{{ troop.level }}</small>
      </troop>
    </div>

    <div class="column is-3">
      <h4 class="title is-4 is-marginless">Spells</h4>
      <troop v-for="spell in player.spells" :key="spell.name" :name="spell.name">
        <small :class="{ max: spell.maxLevel == spell.level }">{{ spell.level }}</small>
      </troop>
    </div>
    <div class="column is-3">
      <h4 class="title is-4 is-marginless">Heros</h4>
      <troop v-for="hero in filterTroops(player.heroes, 'home')" :key="hero.name" :name="hero.name">
        <small :class="{ max: hero.maxLevel == hero.level }">{{ hero.level }}</small>
      </troop>
      <h4 class="subtitle is-5 is-marginless">Builder Base</h4>
      <troop v-for="hero in filterTroops(player.heroes, 'builderBase')" :key="hero.name" :name="hero.name">
        <small :class="{ max: hero.maxLevel == hero.level }">{{ hero.level }}</small>
      </troop>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import Troop from "./Troop";

export default {
  props: [],
  components: {
    Troop,
  },
  data() {
    return {};
  },
  computed: {
    ...mapState(["player"]),
  },
  methods: {
    filterTroops(list, type) {
      return list.filter((troop) => troop.village == type);
    },
  },
};
</script>

<style lang="scss" scoped>
::v-deep .troop {
  margin: 2px;
  position: relative;
  cursor: default;

  small {
    font-size: 0.7em;
    position: absolute;
    right: 2px;
    bottom: 1px;
    color: white;
    background-color: #333;
    padding: 0 1px;
    border-radius: 2px;
    min-width: 14px;
    text-align: center;

    &.max {
      background-color: #ffdd57;
      color: #333;
    }
  }
}
</style>
