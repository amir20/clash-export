<template>
  <div class="box">
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
      data: {
        badgeUrls: {
          small: "https://placeholdit.co//i/500x500?text=&bg=ccc"
        },
        name: "██████",
        tag: "██████",
        clanPoints: "0"    
      }
    };
  },
  async created() {    
    this.data = await (await fetch(`/clan/${this.tag.replace("#", "")}/short.json`)).json();
  }
};
</script>
