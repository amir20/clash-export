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
          <card :tag="savedTag" @error="onClanError" :foundClan.sync="foundClan"></card>
          <p class="buttons">
            <button type="reset" class="button is-warning is-large">Change Clan</button>
            <a :href="`/clan/${foundClan.slug}`" class="button is-success is-large" :disabled="foundClan.slug == null">Continue &rsaquo;</a>
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
                    <search-box :selected-tag.sync="savedTag" size="is-large"></search-box>
                </p>
            </div>
        </template>
    </form>
</template>

<script>
import Card from "./ClanCard";
import SearchBox from "./SearchBox";

const STORAGE_KEY = "lastTag";

export default {
  components: {
    Card,
    SearchBox
  },
  data() {
    return {
      savedTag: null,
      foundClan: { slug: null }
    };
  },
  created() {
    this.savedTag = localStorage.getItem(STORAGE_KEY);
    if (this.savedTag) {
      console.log(`Found saved tag value [${this.savedTag}].`);
      this.prefetch(`${this.url}.json`);
      this.prefetch(`${this.url}.json?daysAgo=7`);
    }
  },
  methods: {
    onReset() {
      this.savedTag = null;
      this.tag = null;
    },
    onClanError() {
      this.savedTag = null;
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
    url() {
      return this.savedTag ? `/clan/${this.savedTag.replace("#", "")}` : "";
    }
  },
  watch: {
    savedTag(newValue) {
      try {
        if (newValue == null) {
          localStorage.removeItem(STORAGE_KEY);
        } else {
          localStorage.setItem(STORAGE_KEY, newValue);
        }
      } catch (e) {
        // Do nothing as some browsers block this in private mode
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
