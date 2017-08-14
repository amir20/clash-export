const STORAGE_KEY = "lastTag";
const input = document.querySelector("input#tag");

document.querySelector("form").addEventListener("submit", () => {
  localStorage.setItem(STORAGE_KEY, input.value);
});

if (localStorage.getItem(STORAGE_KEY)) {
  const tag = localStorage.getItem(STORAGE_KEY);
  console.log(`Found last tag value [${tag}].`);
  input.value = tag;
}
