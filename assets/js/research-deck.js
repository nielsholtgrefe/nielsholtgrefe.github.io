/* Research themes as a stacked "deck of cards" carousel.
   Progressive enhancement: without JS the cards render as a normal vertical
   stack (see .theme-deck in custom-pages.css). This script switches the deck
   into the interactive stacked mode and wires up prev/next, dots, keyboard,
   drag/swipe, and dynamic height (so the plain-language folds can still expand). */
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
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  deck.classList.add("js-deck");
  var controls = deck.querySelector(".deck-controls");
  if (controls) controls.removeAttribute("aria-hidden");

  function setHeight() {
    // Stage height follows the active card so the layout below stays put and
    // the card can grow/shrink when a plain-language fold is toggled.
    stage.style.height = cards[active].offsetHeight + "px";
  }

  // Left-to-right deck: the active card sits in front, the rest of the deck fans
  // out to the RIGHT (clearly visible + clickable); already-seen cards slide off
  // to the left. Offsets scale with the stage width so nothing overflows.
  var OFFSET = [0, 30, 54, 74];
  var SCALE = [1, 0.955, 0.915, 0.88];
  var YY = [0, 8, 16, 24];
  var OP = [1, 0.85, 0.62, 0.42];

  function layout() {
    var k = Math.min(1, (stage.clientWidth || 640) / 640);
    cards.forEach(function (card, i) {
      var p = i - active;
      var transform, opacity, z;
      if (p === 0) {
        transform = "translateX(0) translateY(0) scale(1)";
        opacity = 1; z = 100;
      } else if (p > 0 && p <= 3) {
        transform = "translateX(" + (OFFSET[p] * k) + "px) translateY(" + YY[p] + "px) scale(" + SCALE[p] + ")";
        opacity = OP[p]; z = 100 - p;
      } else if (p > 3) {
        transform = "translateX(" + (OFFSET[3] * k + 24) + "px) scale(0.86)";
        opacity = 0; z = 100 - p;
      } else {
        transform = "translateX(-26px) translateY(6px) scale(0.92)";
        opacity = 0; z = 0;
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
    setHeight();
  }

  function go(i) {
    active = Math.max(0, Math.min(cards.length - 1, i));
    layout();
  }
  function next() { if (active < cards.length - 1) go(active + 1); }
  function prev() { if (active > 0) go(active - 1); }

  if (nextBtn) nextBtn.addEventListener("click", next);
  if (prevBtn) prevBtn.addEventListener("click", prev);
  dots.forEach(function (dot) {
    dot.addEventListener("click", function () { go(parseInt(dot.dataset.goto, 10) || 0); });
  });

  // Click a peeking card to bring it forward.
  cards.forEach(function (card, i) {
    card.addEventListener("click", function (e) {
      if (i !== active && !e.target.closest("a, button, summary")) { e.preventDefault(); go(i); }
    });
  });

  // Keyboard when the deck has focus.
  deck.tabIndex = 0;
  deck.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { next(); e.preventDefault(); }
    else if (e.key === "ArrowLeft") { prev(); e.preventDefault(); }
  });

  // Pointer drag / swipe.
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

  // Keep height correct when a fold opens/closes or the viewport resizes.
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(function () { setHeight(); });
    cards.forEach(function (c) { ro.observe(c); });
  } else {
    deck.addEventListener("toggle", setHeight, true);
  }
  window.addEventListener("resize", layout);
  window.addEventListener("load", setHeight);

  layout();
})();
