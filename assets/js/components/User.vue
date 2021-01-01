<template>
  <b-dropdown position="is-bottom-left" v-if="hasUser">
    <a class="navbar-item button is-transparent" slot="trigger">
      <b-icon pack="fas" icon="user" size="is-small" class="user"></b-icon>
      <span>{{ userName }}</span>
      <b-icon pack="fas" icon="angle-down" size="is-small"></b-icon>
    </a>
    <template v-if="userData">
      <b-dropdown-item has-link>
        <a :href="`/clan/${userData.clan.slug}`">{{ userData.clan.name }}</a>
      </b-dropdown-item>
      <b-dropdown-item has-link> <a :href="`/player/${userSlug}`">Your profile</a> </b-dropdown-item>
      <b-dropdown-item separator></b-dropdown-item>
      <b-dropdown-item has-link> <a @click="removeUser">Forget Me</a> </b-dropdown-item>
    </template>
  </b-dropdown>
</template>

<style scoped>
.button.is-transparent {
  background: transparent;
  border-color: transparent;
}
</style>
<script>
import UserMixin from "../user";

export default {
  mixins: [UserMixin],
};
</script>
