import Vue from "vue";
import Buefy from "buefy";
import Home from "./components/Home"

Vue.use(Buefy);

new Vue({
  el: "#home",  
  components: {
    Home
  }  
});

