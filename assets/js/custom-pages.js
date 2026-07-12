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
   pubRender() reconciles the tag filter and the sort mode. Sorting/grouping
   applies only to the main section (.pub-main); theses and miscellaneous keep
   their own sections at the bottom, so their anchors stay valid. Dividers are
   regenerated per sort: year labels (newest/oldest) or type labels (type). */
let pubCurrentTag = "all";
let pubCurrentSort = "year";
let pubMainOriginal = null;

const PUB_TYPE_LABELS = {
  journal: "Journal articles",
  preprint: "Preprints",
  conference: "Conference papers",
};
const PUB_TYPE_RANK = { journal: 0, conference: 1, preprint: 2 };

function pubMakeDivider(text) {
  const d = document.createElement("div");
  d.className = "year-label js-divider";
  const s = document.createElement("span");
  s.textContent = text;
  d.appendChild(s);
  return d;
}

function pubRender() {
  const list = document.querySelector(".pub-list");
  const main = document.querySelector(".pub-main");
  if (!list || !main) return;
  if (!pubMainOriginal) pubMainOriginal = Array.from(main.children);

  // 1) Apply the tag filter across every entry (main, theses, miscellaneous)
  let anyVisible = false;
  list.querySelectorAll(".pub-item").forEach((item) => {
    const tags = (item.dataset.tags || "").split(/\s+/).filter(Boolean);
    const show = pubCurrentTag === "all" || tags.includes(pubCurrentTag);
    item.classList.toggle("noshow", !show);
    if (show) anyVisible = true;
  });

  // 2) Arrange the main section
  main.querySelectorAll(".js-divider").forEach((d) => d.remove());

  if (pubCurrentSort === "year") {
    pubMainOriginal.forEach((node) => main.appendChild(node));
    main.querySelectorAll(".year-label").forEach((l) => l.classList.remove("noshow"));
    pubHideEmptyYearLabels(main);
    main.classList.remove("hide-pubnum");
  } else {
    main.querySelectorAll(".year-label").forEach((l) => l.classList.add("noshow"));
    const items = Array.from(main.querySelectorAll(".pub-item"));
    const byDateDesc = (a, b) => (b.dataset.date || "").localeCompare(a.dataset.date || "");
    const comparators = {
      oldest: (a, b) => (a.dataset.date || "").localeCompare(b.dataset.date || ""),
      title: (a, b) => (a.dataset.title || "").localeCompare(b.dataset.title || ""),
      type: (a, b) => (PUB_TYPE_RANK[a.dataset.type] - PUB_TYPE_RANK[b.dataset.type]) || byDateDesc(a, b),
    };
    items.sort(comparators[pubCurrentSort] || byDateDesc);

    // Oldest keeps year dividers; type gets "Journal articles"-style dividers.
    let lastGroup = null;
    items.forEach((item) => {
      const groupable = pubCurrentSort === "oldest" || pubCurrentSort === "type";
      if (groupable && !item.classList.contains("noshow")) {
        const g = pubCurrentSort === "oldest" ? item.dataset.year : item.dataset.type;
        if (g !== lastGroup) {
          const label = pubCurrentSort === "type" ? (PUB_TYPE_LABELS[g] || g) : g;
          main.appendChild(pubMakeDivider(label));
          lastGroup = g;
        }
      }
      main.appendChild(item);
    });
    // Only A-Z / type break the chronological index numbering, so hide it there.
    main.classList.toggle("hide-pubnum", pubCurrentSort === "title" || pubCurrentSort === "type");
  }

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

function filterPubs(tag, btn) {
  if (tag !== "all" && btn && btn.classList.contains("is-active")) tag = "all";
  pubCurrentTag = tag;
  document.querySelectorAll(".filter-pill").forEach((pill) => {
    pill.classList.toggle("is-active", pill.dataset.filterTag === tag);
  });
  pubRender();
}

function sortPubs(mode, btn) {
  pubCurrentSort = mode;
  document.querySelectorAll(".sort-pill").forEach((pill) => {
    pill.classList.toggle("is-active", pill.dataset.sort === mode);
  });
  pubRender();
}

/* Clicking anywhere on a publication card (except a link or button) toggles
   its abstract. Delegated, so it keeps working after sorting reorders cards. */
document.addEventListener("click", (e) => {
  const card = e.target.closest(".pub-card");
  if (!card) return;
  if (e.target.closest("a, button")) return; // let links/toggles act normally
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
