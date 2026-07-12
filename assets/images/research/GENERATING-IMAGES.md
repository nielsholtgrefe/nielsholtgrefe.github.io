# Research theme figures — image generation brief

The /research/ page shows one small illustrative figure per theme. Drop the generated
PNGs at the exact paths below and they replace the styled placeholder box automatically:

    theme-reconstruction.png   theme-identifiability.png   theme-diversity.png
    theme-parameters.png       theme-theory.png

Figures render ~240px wide at 4:3 (object-fit: cover) on a card that is light teal
(#e4f2f7) in light mode and deep teal (#123742) in dark mode. Paste the prompt below
into an image model (or ask Claude to render SVG/PNG) to generate the full matched set.

---

Produce a COHESIVE SET of 5 minimal technical line-art ("blueprint") research figures for an academic phylogenetics website. Render EACH as its own flat 2D vector illustration exported at 1600x1200 px (4:3), PNG. All five share ONE identical visual system and differ only in subject. No text anywhere.

=========================
STYLE BLOCK — applies identically to all 5
=========================

GROUND (background decision, deliberate and required): Every figure is a SELF-CONTAINED LIGHT TILE. Fill the ENTIRE 1600x1200 canvas edge-to-edge with a single flat, very pale ice-teal ground #F1FAFC (a hair lighter than the site card #e4f2f7). No transparency, no pure white, no gradient, no vignette, no border, no dark background. RATIONALE: the identical PNG must sit on a LIGHT-teal card (#e4f2f7) in light mode AND a DEEP-teal card (#123742) in dark mode, via object-fit:cover. A full-bleed pale tile reads as a clean light illustration panel in BOTH modes — it blends softly into the light card and pops as a crisp bright inset panel on the dark card — so contrast is guaranteed either way with no transparency guesswork.

PALETTE (strict — 1 ground + 2 line tones + 1 accent, nothing else):
- Ground / node fills: #F1FAFC (flat).
- Primary teal ink (dominant linework + node rings): #1a5c7a.
- Mid teal (secondary / de-emphasized / context linework + nodes): #4a8fa8.
- ACCENT warm coral (ONE hero element per figure only, used sparingly — the "answer"): #EF6F53.
- Ink #2a2a2a permitted ONLY for tiny arrowheads if a pure teal arrowhead reads weak; use minimally.
No other hues. No black fills. No warm tones except the single coral accent. Coral appears in every figure but only on the one element carrying that figure's idea, so the eye lands there instantly even at 240px.

STROKE & NODES (must survive downscaling to ~240px wide):
- Monoline strokes only, uniform weight: primary edges ~7 px, mid/context edges ~5 px, accent element ~9 px. Round caps and joins. Clean, confident, even, textbook-precise linework.
- Nodes = small circles: outer ring ~30 px diameter, ring stroke in teal, filled pale #F1FAFC. Standard node = primary teal ring; context node = mid teal ring. Highlighted / hero node = filled solid coral #EF6F53.
- Directed edges: one small neat triangular arrowhead (~20 px) near the child end. Undirected edges: plain lines, no arrowhead.
- Roughly 6–12 nodes per figure. Generous whitespace.

COMPOSITION & MARGINS: Center the motif. Keep all artwork inside a ~140 px safe margin on every side (live area ~1320x920), and keep ALL FOUR CORNERS clear (the card has rounded corners that clip image corners). One clear focal idea per tile. Calm, balanced negative space. Keep roughly the same graph scale and visual density across all five.

MOOD: precise, quiet, mathematical, elegant — like a clean textbook diagram or architectural blueprint. Modern, minimal, tasteful.

=========================
THE 5 FIGURES
=========================

1) FILE: /assets/images/research/theme-reconstruction.png — "Reconstructing Evolutionary Networks":
Assembling one large network from small overlapping 4-leaf pieces. UPPER-LEFT: a loose scatter of 3–4 tiny "quarnet" fragments, each a compact 4-leaf graphlet (4 outer nodes joined by one short internal edge — little cherry/H/diamond shapes), some with subtly notched puzzle-tab edges, a few overlapping as if slotting together. Thin guide lines imply rightward assembly. They converge into ONE larger reticulated phylogenetic network on the right (teal nodes and edges, a couple of reticulation cycles, leaves fanning downward). ACCENT: the single reticulation arc of the assembled network (where two lineages rejoin) is coral #EF6F53 — the reconstructed result. Combinatorial, jigsaw feel: many small pieces → one whole.

2) FILE: /assets/images/research/theme-identifiability.png — "Identifiability and Statistical Foundations":
Can two look-alike networks be told apart from data. Two small near-mirrored reticulated networks placed symmetrically left and right, same node count and near-identical silhouette so they read as look-alikes, separated by a slim central vertical gap. Draw both in primary teal. ACCENT: the ONE edge that differs between them is coral #EF6F53 in BOTH networks, plus a small coral "compare" mark bridging the gap (two dots joined by a short link — purely geometric, NO equals-sign, NO characters). Idea: the tiny distinguishing feature separating otherwise identical structures.

3) FILE: /assets/images/research/theme-diversity.png — "Phylogenetic Diversity and Conservation":
Budgeted subset of species capturing the most diversity. One rooted phylogenetic tree/network filling the frame: root near the top, ~7 leaf nodes fanned along the bottom, a couple of reticulation edges. Most leaves and branches recede in mid teal #4a8fa8 (context). ACCENT: a chosen subset of 3 leaf nodes (filled solid coral #EF6F53) AND the branch paths connecting them back up toward the root drawn in coral — the selected, most-diverse set standing out from the muted rest. A faint thin geometric bracket loosely groups the whole leaf row to suggest the budget.

4) FILE: /assets/images/research/theme-parameters.png — "Structural Parameters and Algorithms":
Scanwidth / sweeping a directed acyclic graph. A tidy DAG in primary teal: nodes in loose horizontal layers, directed edges with small arrowheads flowing downward (top source → bottom sinks), a few reticulation merges. ACCENT: one straight coral #EF6F53 sweep/cut line crossing the graph roughly vertically or gently diagonally, with small coral dots marking exactly where it intersects edges — the current "width" of the cut. A subtle ghosted faint repeat of the sweep-line hints it stepping across. Conveys a traversal order and a width measure. No numbers.

5) FILE: /assets/images/research/theme-theory.png — "Mathematical Theory of Semi-directed Networks":
One elegant MIXED graph (semi-directed network), balanced and almost symmetric, NOT obviously rooted. Combine BOTH edge types within one structure: the upper portion uses plain UNDIRECTED teal edges (no arrowheads — the unknown/unrooted region); the lower portion has DIRECTED edges with clear arrowheads meeting at a reticulation node (known reticulation events). Emphasize the deliberate MIX of arrowed and plain edges as the defining idea. ACCENT: the reticulation — the pair of directed arrows converging on the reticulation node — in coral #EF6F53. Optionally one hollow teal ring node hints "root unknown". Clean, formal, characterization-diagram feel.

=========================
NEGATIVE CONSTRAINTS (all figures)
=========================
NO text, letters, numbers, math symbols, equations, or labels of any kind (they render tiny and garble — represent comparison/equation/order purely with abstract geometry: aligned dots, mirror layout, connectors). NO photorealism, NO 3D, NO drop shadows, NO glow, NO gradients, NO textures or scenery. NO literal DNA double-helix cliché. NO rainbow or extra colors. NO clutter, dense meshes, or clip-art.

=========================
OUTPUT
=========================
Five separate flat-vector PNGs, each 1600x1200 px (4:3), one per filename above, forming ONE matched blueprint series governed entirely by the STYLE BLOCK — identical ground, stroke weights, node style, arrow style, margins, palette, and drawing "hand" — distinguishable ONLY by subject, with exactly one coral #EF6F53 accent per figure.
