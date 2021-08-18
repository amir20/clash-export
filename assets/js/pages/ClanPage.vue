<template>
  <div>
    <section class="hero is-warning">
      <clan-page-header></clan-page-header>
    </section>
    <div class="tabs is-centered is-boxed">
      <ul>
        <router-link :to="{ name: 'players' }" custom v-slot="{ href, navigate, isActive, isExactActive }">
          <li :class="[isActive && '', isExactActive && 'is-active']">
            <a :href="href" @click="navigate">Members</a>
          </li>
        </router-link>
        <router-link :to="{ name: 'cwl' }" custom v-slot="{ href, navigate, isActive, isExactActive }">
          <li :class="[isActive && '', isExactActive && 'is-active']">
            <a :href="href" @click="navigate">Clan League Wars</a>
          </li>
        </router-link>
      </ul>
    </div>
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<script>
import ClanPageHeader from "../components/ClanPageHeader";

export default {
  components: {
    ClanPageHeader,
  },
  name: "ClanPage",
};
</script>
<style lang="scss" scoped>
.tabs {
  width: 100vw;
  position: sticky;
  left: 0;
  margin-bottom: 3px !important;
  background-color: #ffe08a;
}
</style>
