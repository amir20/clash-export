<template>
  <div class="dropdown is-hoverable is-right has-text-left">
    <div class="dropdown-trigger">
      <button class="button is-danger" aria-haspopup="true" aria-controls="dropdown-menu">
        <span class="icon"> <i class="fa fa-download"></i> </span> <span>Export to Excel</span>
        <span class="icon is-small"> <i class="fa fa-angle-down" aria-hidden="true"></i> </span>
      </button>
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
import { csrfToken } from "../client";

export default {
  data() {
    return {};
  },
  computed: {
    ...mapState(["clan"]),
  },
  methods: {
    async download(event, daysAgo) {
      event.preventDefault();
      const blob = await (
        await fetch(`/clan/download`, {
          method: "POST",
          body: JSON.stringify({ tag: this.clan.tag, daysAgo }),
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
        })
      ).blob();

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
