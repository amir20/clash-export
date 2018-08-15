<template>
<b-dropdown class="updates" position="is-bottom-left">
  <a class="navbar-item" slot="trigger" @click="onMenuClick">
      <span class="badge is-badge-warning is-badge-small" ref="badge">
        Updates
      </span>
  </a>

  <b-dropdown-item custom v-for="item in items" :key="item.sys.id">
      <strong>{{ item.fields.title }}</strong>
      <span class="has-text-weight-light">{{ item.fields.summary }}</span>
      <br>
      <a :href="`/updates#${item.fields.slug}`">Read More</a>
  </b-dropdown-item>

  <b-dropdown-item separator></b-dropdown-item>

  <b-dropdown-item custom paddingless>
    <a href="/updates" class="button is-text is-fullwidth is-small more">See all</a>
  </b-dropdown-item>
</b-dropdown>
</template>

<style scoped>
.updates /deep/ .dropdown-menu {
  min-width: 20em;
}
</style>

<script>
const KEY = "changelog";

export default {
  data() {
    return { items: [] };
  },
  created() {
    this.items = this.data = window.__CHANGELOG__;
  },
  mounted() {
    if (localStorage.getItem(KEY) != this.items[0].sys.id) {
      this.showBadge();
    }
  },
  methods: {
    onMenuClick() {
      try {
        localStorage.setItem(KEY, this.items[0].sys.id);
      } catch (e) {}
      this.hideBadge();
    },
    showBadge() {
      this.$refs.badge.dataset.badge = "";
    },
    hideBadge() {
      delete this.$refs.badge.dataset.badge;
    }
  }
};
</script>
