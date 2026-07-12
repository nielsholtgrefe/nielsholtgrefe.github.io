/* Fluent conferences timeline.
   As you scroll, a focal band near the top-third of the viewport stays put and
   the entries flow through it: the entry nearest the band is fully lit and
   slightly larger, while entries further away dim and shrink a touch. This gives
   the same "stay in place, content flows by" feel as the card decks.

   Progressive enhancement: without JS (or with reduced-motion) the entries just
   render as a normal, fully-visible timeline. */
(function () {
  var tl = document.querySelector(".timeline");
  if (!tl) return;
  var entries = Array.prototype.slice.call(tl.querySelectorAll(".timeline-entry"));
  if (entries.length < 2) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  tl.classList.add("js-timeline");

  function clearAll() {
    entries.forEach(function (en) {
      var card = en.querySelector(".timeline-card");
      if (card) { card.style.opacity = ""; card.style.transform = ""; }
      en.classList.remove("is-focus");
    });
  }

  var ticking = false;
  function update() {
    ticking = false;
    var vh = window.innerHeight || document.documentElement.clientHeight;
    var maxScroll = (document.documentElement.scrollHeight || 0) - vh;
    // On a page that barely scrolls there is no room to flow entries through the
    // band, so just show everything at full strength.
    if (maxScroll < 40) { clearAll(); return; }

    var scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
    var atTop = scrollY <= 2;
    var atBottom = scrollY >= maxScroll - 2;
    var focus = vh * 0.4;            // the focal line: ~40% down the viewport
    var range = vh * 0.55;           // distance over which entries fade out
    var nearBand = vh * 0.14;        // within this, an entry is "in focus"

    entries.forEach(function (en) {
      var card = en.querySelector(".timeline-card");
      if (!card) return;
      var r = en.getBoundingClientRect();
      var mid = r.top + r.height / 2;
      var dist = Math.abs(mid - focus);
      var t = Math.min(1, dist / range);        // 0 at focus … 1 far away
      // At the scroll extremes the entries beyond the band can never reach it,
      // so light them fully: top entries at the top, bottom entries at the bottom.
      if ((atTop && mid <= focus) || (atBottom && mid >= focus)) { t = 0; dist = 0; }
      var opacity = 1 - 0.5 * t;                // 1.0 … 0.5
      var scale = 1 - 0.05 * t;                 // 1.0 … 0.95
      var shift = 12 * t;                       // px, pushed right when far
      card.style.opacity = opacity.toFixed(3);
      card.style.transform = "translateX(" + shift.toFixed(1) + "px) scale(" + scale.toFixed(3) + ")";
      en.classList.toggle("is-focus", dist < nearBand);
    });
  }

  function onScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  window.addEventListener("load", update);
  update();
})();
