<template>
  <b-autocomplete
    placeholder="Search by name or tag"
    field="tag"
    :size="size"
    icon="search"
    icon-pack="fa"
    keep-first
    expanded
    v-model="tag"
    :data="data"
    :loading="isLoading"
    @input="fetchData"
    @select="(option) => this.$emit('update:selectedTag', option ? option.tag : null)"
  >
    <template slot-scope="props">
      <div class="media">
        <div class="media-left"><img width="32" :src="props.option.badge" /></div>
        <div class="media-content">
          <strong>{{ props.option.name }}</strong> <small> <i class="fa fa-tag"></i> {{ props.option.tag }} </small>
          <br />
          <small> <i class="fa fa-users"></i> {{ props.option.members }} members </small>
        </div>
      </div>
    </template>
  </b-autocomplete>
</template>

<script>
import debounce from "lodash/debounce";
import { bugsnagClient } from "../bugsnag";
import { csrfToken } from "../client";

export default {
  props: { size: { type: String } },
  data() {
    return {
      tag: null,
      isLoading: false,
      data: [],
    };
  },
  methods: {
    fetchData: debounce(async function () {
      this.data = [];
      this.isLoading = true;

      try {
        const q = this.tag.replace("#", "");
        this.data = await (
          await fetch(`/search.json`, {
            method: "POST",
            body: JSON.stringify({ q }),
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken(),
            },
          })
        ).json();
      } catch (e) {
        console.error(e);
        bugsnagClient.notify(e);
      }

      this.isLoading = false;
    }, 600),
  },
};
</script>
