<template>
    <form class="section" action="/search" method="get" @reset="onReset">        
        <template v-if="savedTag">   
          <section class="hero">
                <div class="hero-body">
                    <h1 class="title is-1">
                        Welcome Back, Chief!
                    </h1>
                    <h2 class="subtitle">
                        Let's continue with the last clan you viewed or start over again. 
                    </h2>
                </div>
            </section>       
          <Card :tag="savedTag" @error="onClanError" :foundClan.sync="foundClan"/>            
          <p class="buttons">             
            <button type="reset" class="button is-warning is-large">Change Clan</button>
            <a :href="`/clan/${foundClan.slug}`" class="button is-success is-large">Continue &rsaquo;</a>      
          </p>
        </template>
        <template v-else>
          <section class="hero">
                <div class="hero-body">
                    <h1 class="title is-1">
                        Hey, Chief!
                    </h1>
                    <h2 class="subtitle">
                        Welcome to ClashStats. I can find and export all your stats for you. Let's search for your clan by name or tag.                                                 
                    </h2>
                </div>
            </section>
            <div class="column field">
                <p class="control">                    
                    <b-autocomplete
                        placeholder="Clan name or tag"
                        field="tag"
                        size="is-large"
                        keep-first
                        expanded
                        v-model="tag"
                        :data="data"                        
                        :loading="isLoading"
                        @input="fetchData"
                        @select="option => savedTag = option.tag">
                        <template slot-scope="props">
                            <div class="media">
                                <div class="media-left">
                                    <img width="32" :src="props.option.badge">
                                </div>
                                <div class="media-content">
                                    {{ props.option.name }}
                                    <br>
                                    <small>
                                        {{ props.option.tag }}
                                    </small>
                                </div>
                            </div>
                        </template>
                    </b-autocomplete>
                </p>                
            </div>
        </template>    
    </form>
</template>

<script>
import Card from "./ClanCard";
import debounce from "lodash/debounce";

const STORAGE_KEY = "lastTag";

export default {
  components: {
    Card
  },
  data() {
    return {
      savedTag: null,
      tag: null,
      isLoading: false,
      data: [],
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
    fetchData: debounce(async function() {
      this.data = [];
      this.isLoading = true;

      try {
        const query = this.tag.replace("#", "");
        this.data = await (await fetch(`/search.json?q=${query}`)).json();
      } catch (e) {
        console.error(e);
      }

      this.isLoading = false;
    }, 500),
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
      if (newValue == null) {
        localStorage.removeItem(STORAGE_KEY);
      } else {
        localStorage.setItem(STORAGE_KEY, newValue);
      }
    }
  }
};
</script>

