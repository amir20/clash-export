<template>
  <div>
    <section class="hero is-warning">
      <clan-page-header></clan-page-header>
      <div class="hero-footer">
        <router-link :to="{ name: 'players' }">Member Details</router-link>
        <router-link :to="{ name: 'cwl' }">CWL Analytics</router-link>
      </div>
    </section>
    <router-view></router-view>
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
<style lang="scss" scoped></style>
