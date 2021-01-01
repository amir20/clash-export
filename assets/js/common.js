import formatDistance from "date-fns/formatDistance";
import parse from "date-fns/parse";

const items = document.querySelectorAll("[data-from-now]");
[].forEach.call(
  items,
  (i) =>
    (i.innerHTML = formatDistance(parse(i.dataset.fromNow, "yyyy-MM-dd HH:mm:ss", new Date()), new Date(), {
      addSuffix: true,
    }))
);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/static/service-worker.js");
  });
}

import("./fragments/header");
