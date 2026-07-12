/* Generic card-deck carousel, used by the Research and Software pages.
   Each deck is an element carrying data-deck-variant:
     "tuck" — active card near full width; neighbours peek a sliver (research,
              where the previous card tucks behind the profile sidebar).
     "fan"  — coverflow; neighbours are shown more, tilted in the background
              (software, whose cards are narrower).
   Progressive enhancement: without JS the cards render as a normal vertical
   stack. Navigate with prev/next, dots, keyboard, drag/swipe, sideways scroll,
   or by clicking a side card. All cards are sized to the tallest one. */
(function () {
  function initDeck(deck) {
    var stage = deck.querySelector(".deck-stage");
    if (!stage) return;
    var cards = Array.prototype.slice.call(deck.querySelectorAll(".deck-card"));
    if (cards.length < 2) return;

    var dots = Array.prototype.slice.call(deck.querySelectorAll(".deck-dot"));
    var prevBtn = deck.querySelector(".deck-prev");
    var nextBtn = deck.querySelector(".deck-next");
    var variant = deck.dataset.deckVariant || "fan";
    var active = 0;

    deck.classList.add("js-deck");
    var controls = deck.querySelector(".deck-controls");
    if (controls) controls.removeAttribute("aria-hidden");

    function equalizeHeight() {
      var max = 0;
      cards.forEach(function (c) { c.style.height = "auto"; });
      cards.forEach(function (c) { max = Math.max(max, c.offsetHeight); });
      cards.forEach(function (c) { c.style.height = max + "px"; });
      stage.style.height = max + "px";
    }

    // Returns [transform, opacity, zIndex] for a card at signed distance p.
    function place(p) {
      var dir = p < 0 ? -1 : 1;
      var ap = Math.abs(p);
      if (variant === "tuck") {
        if (p === 0) return ["translateX(0) rotateY(0deg) scale(1)", 1, 100];
        if (ap === 1) return ["translateX(" + dir * 90 + "px) rotateY(" + (-dir * 8) + "deg) scale(0.955)", 0.85, 99];
        return ["translateX(" + dir * 130 + "px) rotateY(" + (-dir * 10) + "deg) scale(0.92)", 0, 98];
      }
      // fan
      var W = stage.clientWidth || 640;
      if (p === 0) return ["translateX(0) rotateY(0deg) scale(1)", 1, 100];
      if (ap === 1) return ["translateX(" + dir * 0.5 * W + "px) rotateY(" + (-dir * 16) + "deg) scale(0.86)", 0.72, 99];
      if (ap === 2) return ["translateX(" + dir * 0.76 * W + "px) rotateY(" + (-dir * 20) + "deg) scale(0.76)", 0.34, 98];
      return ["translateX(" + dir * W + "px) rotateY(" + (-dir * 22) + "deg) scale(0.68)", 0, 97];
    }

    function layout() {
      cards.forEach(function (card, i) {
        var pos = place(i - active);
        card.classList.toggle("is-active", i === active);
        card.style.transform = pos[0];
        card.style.opacity = pos[1];
        card.style.zIndex = pos[2];
        card.style.pointerEvents = pos[1] > 0 ? "auto" : "none";
        card.setAttribute("aria-hidden", i === active ? "false" : "true");
      });
      dots.forEach(function (dot, i) {
        dot.classList.toggle("is-active", i === active);
        dot.setAttribute("aria-current", i === active ? "true" : "false");
      });
      if (prevBtn) prevBtn.disabled = active === 0;
      if (nextBtn) nextBtn.disabled = active === cards.length - 1;
    }

    function go(i) { active = Math.max(0, Math.min(cards.length - 1, i)); layout(); }
    function next() { if (active < cards.length - 1) go(active + 1); }
    function prev() { if (active > 0) go(active - 1); }

    if (nextBtn) nextBtn.addEventListener("click", next);
    if (prevBtn) prevBtn.addEventListener("click", prev);
    dots.forEach(function (dot) {
      dot.addEventListener("click", function () { go(parseInt(dot.dataset.goto, 10) || 0); });
    });
    cards.forEach(function (card, i) {
      card.addEventListener("click", function (e) {
        if (i !== active && !e.target.closest("a, button, summary")) { e.preventDefault(); go(i); }
      });
    });

    deck.tabIndex = 0;
    deck.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { next(); e.preventDefault(); }
      else if (e.key === "ArrowLeft") { prev(); e.preventDefault(); }
    });

    var startX = null, startY = null, dragging = false;
    stage.addEventListener("pointerdown", function (e) { startX = e.clientX; startY = e.clientY; dragging = true; });
    window.addEventListener("pointerup", function (e) {
      if (!dragging || startX === null) return;
      dragging = false;
      var dx = e.clientX - startX, dy = e.clientY - startY;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) { dx < 0 ? next() : prev(); }
      startX = startY = null;
    });

    var wheelLock = false;
    stage.addEventListener("wheel", function (e) {
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY) + 4) {
        e.preventDefault();
        if (wheelLock) return;
        if (Math.abs(e.deltaX) > 18) {
          wheelLock = true;
          e.deltaX > 0 ? next() : prev();
          setTimeout(function () { wheelLock = false; }, 450);
        }
      }
    }, { passive: false });

    function refresh() { equalizeHeight(); layout(); }
    refresh();
    window.addEventListener("load", refresh);
    window.addEventListener("resize", refresh);
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-deck-variant]"), initDeck);
})();
