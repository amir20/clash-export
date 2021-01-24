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
        <a class="dropdown-item" @click="download($event, 0)"> Today </a>
        <hr class="dropdown-divider" />
        <a class="dropdown-item" @click="download($event, 1)"> Yesterday </a>
        <a class="dropdown-item" @click="download($event, 2)"> Two Days Ago </a>
        <a class="dropdown-item" @click="download($event, 3)"> Three Days Ago </a>
        <hr class="dropdown-divider" />
        <a class="dropdown-item" @click="download($event, 7)"> Last Week </a>
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

      const file = new File([blob], `${this.clan.tag}.xslx`, { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
      const url = URL.createObjectURL(file);
      window.location.assign(url);
      // URL.revokeObjectURL(url);
    },
  },
};
</script>
<style lang="scss" scoped></style>
