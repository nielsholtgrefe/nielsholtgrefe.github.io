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
   pubRender() reconciles the type filter and the sort mode. Both apply to the
   whole page: the main list, the theses and the miscellaneous section are each
   re-ordered, but every entry stays under its own heading (so the #theses and
   #misc anchors keep working). Only the main list carries year dividers. */
let pubCurrentType = "all";
let pubCurrentSort = "year";
const pubOriginal = new WeakMap();   // section -> its original child order

function pubSortSection(section) {
  if (!section) return;
  if (!pubOriginal.has(section)) pubOriginal.set(section, Array.from(section.children));

  if (pubCurrentSort === "year") {
    // restore the order Jekyll emitted (newest first, dividers in place)
    pubOriginal.get(section).forEach((node) => section.appendChild(node));
  } else {
    // oldest first; re-home each year divider above its first entry
    const items = Array.from(section.querySelectorAll(".pub-item"));
    items.sort((a, b) => (a.dataset.date || "").localeCompare(b.dataset.date || ""));
    const labels = Array.from(section.querySelectorAll(".year-label"));
    labels.forEach((l) => section.appendChild(l));
    let lastYear = null;
    items.forEach((item) => {
      if (!item.classList.contains("noshow") && item.dataset.year !== lastYear) {
        const label = labels.find((l) => (l.textContent || "").trim() === item.dataset.year);
        if (label) section.appendChild(label);
        lastYear = item.dataset.year;
      }
      section.appendChild(item);
    });
  }
  section.querySelectorAll(".year-label").forEach((l) => l.classList.remove("noshow"));
  pubHideEmptyYearLabels(section);
}

function pubRender() {
  const list = document.querySelector(".pub-list");
  if (!list) return;

  // 1) Apply the type filter across every entry (main, theses, miscellaneous)
  let anyVisible = false;
  list.querySelectorAll(".pub-item").forEach((item) => {
    const show = pubCurrentType === "all" || item.dataset.type === pubCurrentType;
    item.classList.toggle("noshow", !show);
    if (show) anyVisible = true;
  });

  // 2) Sort every section, each keeping its own heading
  [".pub-main", ".pub-theses", ".pub-misc"].forEach((sel) =>
    pubSortSection(document.querySelector(sel)));

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
