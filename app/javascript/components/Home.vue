<template>
    <form class="section" action="/search" method="get" @submit="onSubmit" @reset="onReset">        
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
          <Card :tag="savedTag" />            
          <p class="buttons">             
            <button type="reset" class="button is-warning is-large">Change Clan</button>
            <a :href="url" class="button is-success is-large">Continue &rsaquo;</a>      
          </p>
        </template>
        <template v-else>
          <section class="hero">
                <div class="hero-body">
                    <h1 class="title is-1">
                        Hey, Chief!
                    </h1>
                    <h2 class="subtitle">
                        I can help you find your clan and export all your member achievements. Let's start by finding your clan with a
                        <strong>tag</strong>. 
                    </h2>
                </div>
            </section>
            <div class="column field has-addons">
                <p class="control">
                    <input type="text" class="input is-large" placeholder="#tag" v-model="inputModel" name="tag" ref="tag" required>
                </p>
                <p class="control">
                    <button type="submit" class="button is-primary is-large">Go</button>
                </p>
            </div>
        </template>    
    </form>
</template>

<script>
import Card from "./ClanCard";

const STORAGE_KEY = "lastTag";

export default {
  components: {
    Card
  },
  data() {
    return {
      savedTag: null,
      inputModel: ""
    };
  },
  created() {
    this.savedTag = localStorage.getItem(STORAGE_KEY);
    console.log(`Found saved tag value [${this.savedTag}].`);
  },
  methods: {
    onSubmit() {
      localStorage.setItem(STORAGE_KEY, this.inputModel);
    },
    onReset() {
      this.savedTag = null;
      setTimeout((() => this.$refs.tag.focus()).bind(this), 0);
      return false;
    }
  },
  computed: {
    url() {
      return this.savedTag ? `/clan/${this.savedTag.replace("#", "")}` : "";
    }
  }
};
</script>

