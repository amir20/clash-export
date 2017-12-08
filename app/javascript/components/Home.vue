<template>
    <form class="section columns" action="/search" method="get" @submit="onSubmit" @reset="onReset">        
        <template v-if="savedTag">
            <div class="column">
                <Card :tag="savedTag" />
            </div>
            <div class="column buttons">
                <a :href="url" class="button is-success is-large">Continue &rsaquo;</a>   
                <br>             
                <button type="reset" class="button is-danger is-large">Reset</button>
            </div>
        </template>
        <template v-else>
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
      return this.savedTag ? `/clan/${this.savedTag.replace("#", "")}` : '';
    }
  }
};
</script>

<style scoped>

</style>

