/* Contribution filter for the conferences timeline.

   Mirrors the publications page: a row of pills narrows the list to the events
   where I organized, gave a talk, or presented a poster. Every kind of talk
   (lightning, seminar, paper spotlight, ...) is bucketed as "talk" by the
   conf_kinds.html include, which writes the buckets into data-contrib.

   Year markers with no visible event underneath are hidden too, so the timeline
   never shows an empty year. */
(function () {
  var current = "all";

  function entries() {
    return Array.prototype.slice.call(document.querySelectorAll(".timeline-entry"));
  }

  function matches(entry) {
    if (current === "all") return true;
    var kinds = (entry.getAttribute("data-contrib") || "").split(/\s+/);
    return kinds.indexOf(current) !== -1;
  }

  /* A year marker is shown only while some event between it and the next marker
     survives the filter. */
  function syncYears() {
    var tl = document.querySelector(".timeline");
    if (!tl) return;
    var children = Array.prototype.slice.call(tl.children);
    children.forEach(function (el, i) {
      if (!el.classList.contains("timeline-year")) return;
      var visible = false;
      for (var j = i + 1; j < children.length; j++) {
        if (children[j].classList.contains("timeline-year")) break;
        if (children[j].classList.contains("timeline-entry") &&
            !children[j].classList.contains("noshow")) { visible = true; break; }
      }
      el.classList.toggle("noshow", !visible);
    });
  }

  function render() {
    var any = false;
    entries().forEach(function (entry) {
      var show = matches(entry);
      entry.classList.toggle("noshow", !show);
      if (show) any = true;
    });
    syncYears();

    var empty = document.querySelector(".conf-filter-empty");
    if (empty) empty.classList.toggle("noshow", any);

    // timeline.js lights entries by their distance from the focal band; the
    // filter just moved them, so ask it to recompute.
    window.dispatchEvent(new Event("scroll"));
  }

  window.filterConfs = function (kind, btn) {
    // Clicking the active pill clears the filter, as on the publications page.
    if (kind !== "all" && btn && btn.classList.contains("is-active")) kind = "all";
    current = kind;
    document.querySelectorAll("[data-filter-contrib]").forEach(function (pill) {
      var on = pill.getAttribute("data-filter-contrib") === kind;
      pill.classList.toggle("is-active", on);
      pill.setAttribute("aria-pressed", on ? "true" : "false");
    });
    render();
  };
})();
