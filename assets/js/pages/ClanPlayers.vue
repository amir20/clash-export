<template>
  <section>
    <div class="tools">
      <table-nav></table-nav>
    </div>
    <clan-table></clan-table>
  </section>
</template>

<script>
import ClanTable from "../components/ClanTable";
import TableNav from "../components/TableNav";
export default {
  components: {
    ClanTable,
    TableNav,
  },
  name: "ClanPlayers",
};
</script>
<style lang="scss" scoped>
.tools {
  width: 100vw;
  position: sticky;
  left: 0;
  padding: 0.6em 1em;
}
</style>
