import Vue from "vue";
import ClanTag from "./components/ClanTag";
import ClanCard from "./components/ClanCard";
const STORAGE_KEY = "lastTag";
const input = document.querySelector("input#tag");


let savedTag = localStorage.getItem(STORAGE_KEY);


new Vue({
  el: "#last-tag",  
  components: {
    ClanCard
  },
  data: {
    tag: savedTag
  }
});


document.querySelector("form").addEventListener("submit", () => {
  localStorage.setItem(STORAGE_KEY, input.value);
});

if (localStorage.getItem(STORAGE_KEY)) {
  const tag = localStorage.getItem(STORAGE_KEY);
  console.log(`Found last tag value [${tag}].`);
  input.value = tag;
}


