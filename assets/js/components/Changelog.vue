<template>
  <b-dropdown class="changelog" position="is-bottom-left">
    <a class="navbar-item" slot="trigger" @click="onMenuClick">
      <span class="badge has-badge-warning has-badge-rounded has-badge-small" :data-badge="hasUpdates ? '' : false"> Updates </span>
    </a>

    <b-dropdown-item custom v-for="item in items" :key="item.id">
      <strong>{{ item.title }}</strong> <span class="has-text-weight-light">{{ item.summary }}</span> <br />
      <a :href="`/updates#${item.slug}`">Read More</a>
    </b-dropdown-item>

    <b-dropdown-item separator></b-dropdown-item>

    <b-dropdown-item custom paddingless>
      <a href="/updates" class="button is-text is-fullwidth">See all updates</a>
    </b-dropdown-item>
  </b-dropdown>
</template>

<style lang="scss" scoped>
.changelog /deep/ .dropdown-menu {
  min-width: 20em;
}
</style>

<script>
import store from "store/dist/store.modern";
const KEY = "changelog";

export default {
  data() {
    return { items: [], hasUpdates: false };
  },
  created() {
    this.items = this.data = __UPDATES__;
  },
  mounted() {
    if (store.get(KEY) != this.items[0].id) {
      this.hasUpdates = true;
    }
  },
  methods: {
    onMenuClick() {
      store.set(KEY, this.items[0].id);
      this.hasUpdates = false;
    },
  },
};
</script>
