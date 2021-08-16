<template>
  <div>
    <section class="hero is-warning">
      <clan-page-header></clan-page-header>
      <div class="hero-footer">
        <table-nav></table-nav>
      </div>
    </section>
    <router-view></router-view>
  </div>
</template>

<script>
import ClanPageHeader from "../components/ClanPageHeader";
import TableNav from "../components/TableNav";

export default {
  components: {
    ClanPageHeader,
    TableNav,
  },
  name: "ClanPage",
};
</script>
<style lang="scss" scoped></style>
