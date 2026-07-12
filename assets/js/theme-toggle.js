/* Dark-mode toggle: injects a button into the masthead nav, persists the
   choice in localStorage, and follows the OS preference until the user picks
   manually. The initial theme is set by an inline script in <head> to avoid a
   flash of the wrong theme; this file wires up the interactive parts. */
(function () {
  function currentTheme() {
    return document.documentElement.getAttribute("data-theme") === "dark"
      ? "dark"
      : "light";
  }

  function apply(theme, persist) {
    document.documentElement.setAttribute("data-theme", theme);
    if (persist) {
      try {
        localStorage.setItem("nh-theme", theme);
      } catch (e) {}
    }
    document.querySelectorAll(".nh-theme-toggle").forEach(function (b) {
      b.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      b.title = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
    });
  }

  function inject() {
    var nav = document.querySelector(".greedy-nav");
    if (!nav || nav.querySelector(".nh-theme-toggle")) return;

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "nh-theme-toggle";
    btn.setAttribute("aria-label", "Toggle dark mode");
    btn.innerHTML =
      '<span class="nh-icon-sun" aria-hidden="true">☀</span>' +
      '<span class="nh-icon-moon" aria-hidden="true">☾</span>';
    btn.addEventListener("click", function () {
      apply(currentTheme() === "dark" ? "light" : "dark", true);
    });

    // Place before the overflow toggle (the "..." menu) if present.
    var overflow = nav.querySelector(".greedy-nav__toggle");
    if (overflow) {
      nav.insertBefore(btn, overflow);
    } else {
      nav.appendChild(btn);
    }
    apply(currentTheme(), false);
  }

  // Expose the masthead height so the sticky page banner can sit right below it.
  function setMastheadHeight() {
    var m = document.querySelector(".masthead");
    if (m) {
      document.documentElement.style.setProperty("--nh-masthead-h", m.offsetHeight + "px");
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      inject();
      setMastheadHeight();
    });
  } else {
    inject();
    setMastheadHeight();
  }
  window.addEventListener("load", setMastheadHeight);
  window.addEventListener("resize", setMastheadHeight);

  // Follow system changes only while the user hasn't chosen manually.
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function (e) {
      try {
        if (localStorage.getItem("nh-theme")) return;
      } catch (err) {}
      apply(e.matches ? "dark" : "light", false);
    };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }
})();
