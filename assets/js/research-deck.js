/* Research themes as a "coverflow" deck.
   Progressive enhancement: without JS the cards render as a normal vertical
   stack (see .theme-deck in custom-pages.css). This script switches the deck
   into the interactive coverflow: the active theme sits in the centre, already
   seen ("old") cards stay visible tilted on the LEFT, upcoming cards on the
   RIGHT — all rendered at the same fixed size. Navigate with prev/next, dots,
   keyboard, drag/swipe, sideways scroll, or by clicking a side card. */
(function () {
  var deck = document.getElementById("theme-deck");
  if (!deck) return;
  var stage = document.getElementById("deck-stage");
  var cards = Array.prototype.slice.call(deck.querySelectorAll(".deck-card"));
  if (cards.length < 2) return;

  var dots = Array.prototype.slice.call(deck.querySelectorAll(".deck-dot"));
  var prevBtn = deck.querySelector(".deck-prev");
  var nextBtn = deck.querySelector(".deck-next");
  var active = 0;

  deck.classList.add("js-deck");
  var controls = deck.querySelector(".deck-controls");
  if (controls) controls.removeAttribute("aria-hidden");

  // Make every card the same size: the tallest card's natural height, so shorter
  // ones simply get some whitespace. Measured with the cards briefly auto-height.
  function equalizeHeight() {
    var max = 0;
    cards.forEach(function (c) { c.style.height = "auto"; });
    cards.forEach(function (c) { max = Math.max(max, c.offsetHeight); });
    cards.forEach(function (c) { c.style.height = max + "px"; });
    stage.style.height = max + "px";
  }

  // The active card is (nearly) full width; only the immediate neighbours peek out
  // a small amount behind it — the previous one to the LEFT (tucking behind the
  // profile sidebar), the next one to the RIGHT.
  function layout() {
    cards.forEach(function (card, i) {
      var p = i - active;
      var dir = p < 0 ? -1 : 1;
      var transform, opacity, z;
      if (p === 0) {
        transform = "translateX(0) rotateY(0deg) scale(1)";
        opacity = 1; z = 100;
      } else if (Math.abs(p) === 1) {
        transform = "translateX(" + (dir * 90) + "px) rotateY(" + (-dir * 8) + "deg) scale(0.955)";
        opacity = 0.85; z = 99;
      } else {
        transform = "translateX(" + (dir * 130) + "px) rotateY(" + (-dir * 10) + "deg) scale(0.92)";
        opacity = 0; z = 98;
      }
      card.classList.toggle("is-active", p === 0);
      card.style.transform = transform;
      card.style.opacity = opacity;
      card.style.zIndex = z;
      card.style.pointerEvents = opacity > 0 ? "auto" : "none";
      card.setAttribute("aria-hidden", p === 0 ? "false" : "true");
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

  // Click a side card to bring it to the centre.
  cards.forEach(function (card, i) {
    card.addEventListener("click", function (e) {
      if (i !== active && !e.target.closest("a, button, summary")) { e.preventDefault(); go(i); }
    });
  });

  // Keyboard.
  deck.tabIndex = 0;
  deck.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { next(); e.preventDefault(); }
    else if (e.key === "ArrowLeft") { prev(); e.preventDefault(); }
  });

  // Pointer drag / swipe: dragging the current card left advances (it slides to
  // the left as the "old" card); dragging right goes back.
  var startX = null, startY = null, dragging = false;
  stage.addEventListener("pointerdown", function (e) {
    startX = e.clientX; startY = e.clientY; dragging = true;
  });
  window.addEventListener("pointerup", function (e) {
    if (!dragging || startX === null) return;
    dragging = false;
    var dx = e.clientX - startX, dy = e.clientY - startY;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) { dx < 0 ? next() : prev(); }
    startX = startY = null;
  });

  // Horizontal wheel / trackpad swipe (debounced).
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
})();
