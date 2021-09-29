<template>
  <div class="dropdown is-hoverable is-right has-text-left">
    <div class="dropdown-trigger">
      <b-button type="is-danger" icon-right="fa fa-angle-down" icon-left="fas fa-download"> Export to Excel </b-button>
    </div>
    <div class="dropdown-menu" role="menu">
      <div class="dropdown-content">
        <a class="dropdown-item" @click="download($event, 0)" :href="`${clan.tag}.xlsx`"> Today </a>
        <hr class="dropdown-divider" />
        <a class="dropdown-item" @click="download($event, 1)" :href="`${clan.tag}.xlsx`"> Yesterday </a>
        <a class="dropdown-item" @click="download($event, 2)" :href="`${clan.tag}.xlsx`"> Two Days Ago </a>
        <a class="dropdown-item" @click="download($event, 3)" :href="`${clan.tag}.xlsx`"> Three Days Ago </a>
        <hr class="dropdown-divider" />
        <a class="dropdown-item" @click="download($event, 7)" :href="`${clan.tag}.xlsx`"> Last Week </a>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { gql } from "graphql-request";
import { request } from "../client";
import { event } from "../ga";

export default {
  data() {
    return {};
  },
  computed: {
    ...mapState(["clan"]),
  },
  methods: {
    async download(e, daysAgo) {
      e.preventDefault();
      event("download", `Download ${daysAgo} days ago`);
      const { clan } = await request(
        gql`
          query ExportClan($tag: String!, $days: Int!) {
            clan(tag: $tag) {
              xlsxExport(days: $days)
            }
          }
        `,
        {
          tag: this.clan.tag,
          days: daysAgo,
        }
      );

      const blob = await (await fetch(clan.xlsxExport)).blob();
      const a = document.createElement("a");
      document.body.appendChild(a);
      const url = URL.createObjectURL(blob);
      a.href = url;
      a.download = `${this.clan.tag}.xlsx`;
      a.click();
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }, 0);
    },
  },
};
</script>
<style lang="scss" scoped></style>
