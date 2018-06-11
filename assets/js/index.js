import Vue from "vue";
import Home from "./components/Home";

new Vue({
  el: "#home",
  components: {
    Home
  },
  created() {
    console.log("Created");
  }
});
