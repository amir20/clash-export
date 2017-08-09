const STORAGE_KEY = 'lastTag';

document.querySelector('form').addEventListener('submit', () => {
    const input = document.querySelector('input#tag');
    localStorage.setItem(STORAGE_KEY, input.value);
});

if (localStorage.getItem(STORAGE_KEY)) {
    const tag = localStorage.getItem(STORAGE_KEY);
    console.log(`Found last tag value [${tag}].`)
    const input = document.querySelector('input#tag');
    input.value = tag;
}