<template>
  <section>
    <div>
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
<style lang="scss" scoped></style>
