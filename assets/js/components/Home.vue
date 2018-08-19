<template>
    <form class="section" action="/search" method="get" @reset="onReset">
        <template v-if="savedTag">
          <section class="hero">
                <div class="hero-body">
                    <h1 class="title is-1">
                        Welcome Back, Chief!
                    </h1>
                    <h2 class="subtitle">
                        I found your clan! Let's continue or start over again.
                    </h2>
                </div>
            </section>
          <card :tag="savedTag" @error="onClanError"></card>
          <p class="buttons">
            <button type="reset" class="button is-warning is-large">Change Clan</button>
            <a :href="`/clan/${foundClan ? foundClan.slug : ''}`" class="button is-success is-large" :disabled="foundClan == null">Continue &rsaquo;</a>
          </p>
        </template>
        <template v-else>
          <section class="hero">
                <div class="hero-body">
                    <h1 class="title is-1">
                        Hey, Chief!
                    </h1>
                    <h2 class="subtitle">
                        Welcome to Clash Leaders. This website shows trending clans in Clash of Clans game. 
                        Clan achievements can be exported to a spreadsheet or compared to historical data over time. 
                        Let's start by finding your clan first.
                    </h2>
                </div>
            </section>
            <div class="column field">
                <p class="control">
                    <search-box :selected-tag.sync="selectedTag" size="is-large"></search-box>
                </p>
            </div>
        </template>
    </form>
</template>

<script>
import Card from "./ClanCard";
import SearchBox from "./SearchBox";
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";

export default {
  components: {
    Card,
    SearchBox
  },
  data() {
    return {
      selectedTag: String
    };
  },
  created() {
    if (this.savedTag) {
      console.log(`Found saved tag value [${this.savedTag}].`);
      this.prefetch(`${this.url}/refresh.json`);
      this.prefetch(`${this.url}.json?daysAgo=7`);
    }
  },
  computed: {
    ...mapState(["savedTag"])
  },
  methods: {
    ...mapMutations(["setSavedTag", "clearSavedTag"]),
    onReset() {
      this.clearSavedTag();
    },
    onClanError() {
      this.clearSavedTag();
    },
    prefetch(url) {
      const link = document.createElement("link");
      link.href = url;
      link.rel = "prefetch";
      link.as = "fetch";
      document.head.appendChild(link);
    }
  },
  computed: {
    ...mapState(["foundClan", "savedTag"]),
    url() {
      return this.savedTag ? `/clan/${this.savedTag.replace("#", "")}` : "";
    }
  },
  watch: {
    selectedTag(newValue) {
      if (newValue) {
        this.setSavedTag(newValue);
      }
    }
  }
};
</script>
<style scoped>
a[disabled="disabled"] {
  pointer-events: none;
}
</style>
