/* ---- Toggle a publication's summary / abstract / bibtex box ----
   Only one box is open at a time. The thumbnail lives inside the summary and
   abstract boxes, so it appears automatically when one of them is opened. */
function toggleBox(id) {
  document.querySelectorAll(".abstract-box, .bibtex, .summary-box").forEach((box) => {
    if (box.id !== id) box.classList.add("noshow");
  });

  const box = document.getElementById(id);
  if (box) box.classList.toggle("noshow");
}

/* ---- Publication filtering + sorting (vanilla JS, no dependencies) ----
   pubRender() reconciles the type filter and the sort mode. Sorting/grouping
   applies only to the main section (.pub-main); theses and miscellaneous keep
   their own sections at the bottom, so their anchors stay valid. Year dividers
   are shown for both newest and oldest order. */
let pubCurrentType = "all";
let pubCurrentSort = "year";
let pubMainOriginal = null;

function pubRender() {
  const list = document.querySelector(".pub-list");
  const main = document.querySelector(".pub-main");
  if (!list || !main) return;
  if (!pubMainOriginal) pubMainOriginal = Array.from(main.children);

  // 1) Apply the type filter across every entry (main, theses, miscellaneous)
  let anyVisible = false;
  list.querySelectorAll(".pub-item").forEach((item) => {
    const show = pubCurrentType === "all" || item.dataset.type === pubCurrentType;
    item.classList.toggle("noshow", !show);
    if (show) anyVisible = true;
  });

  // 2) Arrange the main section
  if (pubCurrentSort === "year") {
    pubMainOriginal.forEach((node) => main.appendChild(node));
  } else {
    // oldest: reverse chronological order, keeping year dividers
    const items = Array.from(main.querySelectorAll(".pub-item"));
    items.sort((a, b) => (a.dataset.date || "").localeCompare(b.dataset.date || ""));
    main.querySelectorAll(".year-label").forEach((l) => main.appendChild(l));
    let lastYear = null;
    items.forEach((item) => {
      if (!item.classList.contains("noshow") && item.dataset.year !== lastYear) {
        const label = Array.from(main.querySelectorAll(".year-label"))
          .find((l) => (l.textContent || "").trim() === item.dataset.year);
        if (label) main.appendChild(label);
        lastYear = item.dataset.year;
      }
      main.appendChild(item);
    });
  }
  main.querySelectorAll(".year-label").forEach((l) => l.classList.remove("noshow"));
  pubHideEmptyYearLabels(main);

  // 3) Section headers (theses, misc) shown only when they hold a visible entry
  ["theses", "misc"].forEach((id) => {
    const header = document.getElementById(id);
    if (!header) return;
    const container = header.nextElementSibling;
    const anyIn = container &&
      Array.from(container.querySelectorAll(".pub-item")).some((i) => !i.classList.contains("noshow"));
    header.classList.toggle("noshow", !anyIn);
    if (container) container.classList.toggle("noshow", !anyIn);
  });

  // 4) Empty-state message
  const empty = document.querySelector(".pub-filter-empty");
  if (empty) empty.classList.toggle("noshow", anyVisible);
}

/* Hide year dividers whose year has no visible entry (respecting the filter). */
function pubHideEmptyYearLabels(main) {
  const children = Array.from(main.children);
  children.forEach((el, i) => {
    if (!el.classList.contains("year-label")) return;
    let has = false;
    for (let j = i + 1; j < children.length; j++) {
      const next = children[j];
      if (next.classList.contains("year-label")) break;
      if (next.classList.contains("pub-item") && !next.classList.contains("noshow")) { has = true; break; }
    }
    el.classList.toggle("noshow", !has);
  });
}

function filterPubs(type, btn) {
  if (type !== "all" && btn && btn.classList.contains("is-active")) type = "all";
  pubCurrentType = type;
  document.querySelectorAll(".filter-pill").forEach((pill) => {
    const on = pill.dataset.filterType === type;
    pill.classList.toggle("is-active", on);
    pill.setAttribute("aria-pressed", on ? "true" : "false");
  });
  pubRender();
}

function sortPubs(mode, btn) {
  pubCurrentSort = mode;
  document.querySelectorAll(".sort-pill").forEach((pill) => {
    const on = pill.dataset.sort === mode;
    pill.classList.toggle("is-active", on);
    pill.setAttribute("aria-pressed", on ? "true" : "false");
  });
  pubRender();
}

/* Clicking anywhere on a publication card (except a link or button) toggles
   its abstract. Delegated, so it keeps working after sorting reorders cards. */
document.addEventListener("click", (e) => {
  const card = e.target.closest(".pub-card");
  if (!card) return;
  if (e.target.closest("a, button, .pub-info")) return; // let links/toggles/info icon act normally
  const item = card.closest(".pub-item");
  const abs = item && item.querySelector(".abstract-box");
  if (abs) toggleBox(abs.id);
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".bibtex").forEach((bib) => {
    if (bib.querySelector(".copy-btn")) return;

    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = "📋";
    btn.onclick = () => {
      const pre = bib.querySelector("pre");
      if (!pre) return;
      navigator.clipboard.writeText(pre.innerText).then(() => {
        btn.textContent = "✔️";
        setTimeout(() => {
          btn.textContent = "📋";
        }, 1500);
      });
    };

    bib.appendChild(btn);
  });
});
