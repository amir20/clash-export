<template>
  <div class="box" :class="{'still-loading': loading}">
      <article class="media">
          <div class="media-left">
              <figure class="image is-64x64">
                  <img :src="this.data.badgeUrls.small" alt="Image">
              </figure>
          </div>
          <div class="media-content">
              <div class="content">
                  <p>
                      <strong>{{ this.data.name }}</strong>
                      <i class="fa fa-tag" aria-hidden="true"></i>
                      <small>{{ this.data.tag }}</small>
                      <i class="fa fa-trophy" aria-hidden="true"></i>
                      <small>{{this.data.clanPoints}}</small>
                      <br> {{ this.data.description }}
                  </p>
              </div>
          </div>
      </article>
  </div>
</template>

<script>
export default {
  props: ["tag"],
  data() {
    return {
      loading: true,
      data: {
        badgeUrls: {
          small: "https://placeholdit.co//i/500x500?text=&bg=efefef"
        },
        name: "██████",
        tag: "██████",
        description: "██████ ████████████ █ ████ █ ██████ ████████████ ███ ███",
        clanPoints: "0"
      }
    };
  },
  async created() {
    this.data = await (await fetch(
      `/clan/${this.tag.replace("#", "")}/short.json`
    )).json();
    this.loading = false;
  }
};
</script>
<style scoped>
.still-loading * {
  color: #efefef !important;
}
</style>

