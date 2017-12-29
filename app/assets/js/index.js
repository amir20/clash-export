import Vue from "vue";
import Buefy from "buefy";
import Home from "./components/Home"

Vue.use(Buefy, {defaultIconPack: 'fa'});

new Vue({
  el: "#home",  
  components: {
    Home
  }  
});

