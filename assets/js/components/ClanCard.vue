<template>
  <div class="box" :class="{ 'still-loading': loading }">
    <article class="media">
      <div class="media-left">
        <figure class="image is-64x64"><img :src="this.data.badgeUrls.medium" alt="Image" /></figure>
      </div>
      <div class="media-content">
        <div class="content">
          <p>
            <strong>{{ this.data.name }}</strong>
            <small>
              <i class="fa fa-tag fa-lg" aria-hidden="true"></i> {{ this.data.tag }}
              <i class="fa fa-trophy fa-lg" aria-hidden="true"></i> {{ this.data.clanPoints.toLocaleString() }}
            </small>
            <br />
            {{ this.data.description }}
          </p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
import { bugsnagClient } from "../bugsnag";
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";

export default {
  props: ["tag", "foundClan"],
  data() {
    return {
      loading: true,
      data: {
        badgeUrls: {
          medium: "https://placeholdit.co/i/250x250?text=&bg=efefef"
        },
        name: "██████",
        tag: "██████",
        description: "██████ ████████████ █ ████ █ ██████ ████████████ ███ ███ ███████████ █ ███ ███",
        clanPoints: "0"
      }
    };
  },
  async created() {
    try {
      this.data = await (await fetch(`/clan/${this.tag.replace("#", "")}/short.json`)).json();
    } catch (e) {
      console.error(e);
      bugsnagClient.notify(e);
      this.$emit("error");
    }
    this.$emit("update:foundClan", this.data);
    this.setFoundClan(this.data);
    this.loading = false;
  },
  methods: {
    ...mapMutations(["setFoundClan"])
  }
};
</script>
<style scoped>
.still-loading * {
  color: #efefef !important;
}
</style>
