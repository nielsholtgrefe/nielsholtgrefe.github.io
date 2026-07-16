#!/usr/bin/env python3
"""Generate the research-page figures in Niels' own drawing style.

Outputs (SVG, crisp at any size):
  assets/images/research/theme-reconstruction.svg   MSA -> quarnets -> network
  assets/images/research/theme-identifiability.svg  two nets, same quartets
  assets/images/research/theme-diversity.svg        network + chosen taxa (PD)
  assets/images/research/theme-parameters.svg       network + scanwidth cut
  assets/images/tree-vs-network.svg                 layman tree vs network
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nhstyle import *

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
RES = os.path.join(ROOT, "assets", "images", "research")
IMG = os.path.join(ROOT, "assets", "images")

W, H = 760, 570


def write(path, body):
    open(path, "w").write(body)
    print("wrote", os.path.relpath(path, ROOT), len(body), "bytes")


# --------------------------------------------------------------------------
# A small 4-leaf semi-directed network ("quarnet") drawn his way:
# hollow internal nodes, red dashed arcs into a filled red reticulation.
# --------------------------------------------------------------------------
def quarnet(ox, oy, s=1.0, labels=("1", "2", "3", "4"), tri=False):
    """4-leaf network with a reticulation cycle. Returns svg string."""
    def P(x, y):
        return (ox + x * s, oy + y * s)
    top = P(50, 6)
    a, b = P(20, 40), P(80, 40)
    r = P(50, 66)
    l1, l2 = P(4, 74), P(30, 96)
    l3, l4 = P(70, 96), P(96, 74)
    out = []
    # tree edges
    out.append(edge(top, a)); out.append(edge(top, b))
    out.append(edge(a, l1)); out.append(edge(b, l4))
    out.append(edge(r, l2)); out.append(edge(r, l3))
    # reticulation arcs (red dashed, arrow into r)
    out.append(retic(a, r, bow=6 * s))
    out.append(retic(b, r, bow=-6 * s))
    # nodes
    out.append(node(top, r=4.0 * s)); out.append(node(a, r=4.0 * s)); out.append(node(b, r=4.0 * s))
    out.append(rnode(r, r=4.6 * s))
    for p in (l1, l2, l3, l4):
        out.append(dot(p, r=3.8 * s))
    for p, t in zip((l1, l2, l3, l4), labels):
        dx = -9 * s if p[0] < ox + 50 * s else 9 * s
        out.append(label((p[0] + dx, p[1] + 5 * s), t, size=13 * s))
    return "".join(out)


# --------------------------------------------------------------------------
# 1. RECONSTRUCTION: sequences -> quarnets -> assembled network
# --------------------------------------------------------------------------
def fig_reconstruction():
    o = [header(W, H)]
    o.append(caption((W / 2, 26), "reconstruction: from sequences to a network"))

    # --- stage 1: MSA (monospace, like his fig2) ---
    o.append(box(24, 44, 176, 132))
    seqs = ["-GCG-CACT", "AGCG-C-CT", "-GCCA-AGT", "GCCAA-ATT", "-CGT-ATCT"]
    for i, s in enumerate(seqs):
        o.append(f'<text x="36" y="{72 + i*22}" font-size="15" fill="{BLACK}" '
                 f'font-family="DejaVu Sans Mono, Menlo, monospace">{s}</text>')
    o.append(caption((112, 194), "alignment"))

    # --- stage 2: dense set of quarnets ---
    o.append(box(246, 44, 250, 132))
    o.append(quarnet(258, 62, s=0.86, labels=("1", "2", "3", "4")))
    o.append(quarnet(374, 62, s=0.86, labels=("2", "3", "5", "6")))
    o.append(caption((371, 194), "all 4-leaf quarnets"))

    # --- arrows between stages ---
    o.append(arrow((208, 110), (240, 110)))
    o.append(arrow((504, 110), (536, 110)))

    # --- stage 3: the assembled network (bigger, centre-bottom) ---
    o.append(box(546, 44, 190, 132))
    o.append(quarnet(566, 56, s=1.05, labels=("1", "2", "3", "4")))
    o.append(caption((641, 194), "puzzle them together"))

    # --- big result network underneath ---
    def P(x, y):
        return (x, y)
    root = P(380, 236)
    a, b = P(250, 296), P(510, 296)
    c, d = P(190, 372), P(322, 372)
    e, f = P(438, 372), P(572, 372)
    r1 = P(380, 424)
    leaves = [P(150, 470), P(232, 470), P(300, 470), P(380, 492),
              P(462, 470), P(530, 470), P(612, 470)]
    o.append(edge(root, a)); o.append(edge(root, b))
    o.append(edge(a, c)); o.append(edge(a, d))
    o.append(edge(b, e)); o.append(edge(b, f))
    o.append(edge(c, leaves[0])); o.append(edge(c, leaves[1]))
    o.append(edge(d, leaves[2])); o.append(edge(f, leaves[5])); o.append(edge(f, leaves[6]))
    o.append(edge(e, leaves[4]))
    o.append(edge(r1, leaves[3]))
    o.append(retic(d, r1, bow=10)); o.append(retic(e, r1, bow=-10))
    for p in (root, a, b, c, d, e, f):
        o.append(node(p))
    o.append(rnode(r1))
    for p in leaves:
        o.append(dot(p))
    for p, t in zip(leaves, "1234567"):
        o.append(label((p[0], p[1] + 22), t, size=15))
    o.append(caption((380, 538), "reconstructed semi-directed network"))
    o.append(footer())
    write(os.path.join(RES, "theme-reconstruction.svg"), "".join(o))


# --------------------------------------------------------------------------
# 2. IDENTIFIABILITY: two different networks, indistinguishable data
# --------------------------------------------------------------------------
def fig_identifiability():
    o = [header(W, H)]
    o.append(caption((W / 2, 26), "identifiability: can the data tell them apart?"))

    o.append(box(30, 46, 320, 250))
    o.append(box(410, 46, 320, 250))
    o.append(label((190, 74), "network A", size=16))
    o.append(label((570, 74), "network B", size=16))

    def net_a(ox, oy):
        """Reticulation hangs below a wide 4-cycle."""
        def P(x, y):
            return (ox + x, oy + y)
        top = P(150, 22)
        a, b = P(70, 78), P(230, 78)
        r = P(150, 138)
        l1, l2 = P(24, 178), P(96, 178)
        l3, l4 = P(204, 178), P(276, 178)
        out = [edge(top, a), edge(top, b), edge(a, l1), edge(b, l4),
               edge(r, l2), edge(r, l3),
               retic(a, r, bow=10), retic(b, r, bow=-10)]
        for p in (top, a, b):
            out.append(node(p))
        out.append(rnode(r))
        for p, t in zip((l1, l2, l3, l4), ("1", "2", "3", "4")):
            out.append(dot(p)); out.append(label((p[0], p[1] + 22), t, size=15))
        return "".join(out)

    def net_b(ox, oy):
        """Structurally different: a narrow triangle reticulation on one side."""
        def P(x, y):
            return (ox + x, oy + y)
        top = P(150, 22)
        a = P(96, 74)
        c = P(214, 92)
        r = P(150, 138)
        l1, l2 = P(24, 178), P(112, 178)
        l3, l4 = P(196, 178), P(276, 178)
        out = [edge(top, a), edge(top, c), edge(a, l1), edge(c, l4),
               edge(r, l2), edge(c, l3),
               retic(a, r, bow=12), retic(c, r, bow=-14)]
        for p in (top, a, c):
            out.append(node(p))
        out.append(rnode(r))
        for p, t in zip((l1, l2, l3, l4), ("1", "2", "3", "4")):
            out.append(dot(p)); out.append(label((p[0], p[1] + 22), t, size=15))
        return "".join(out)

    o.append(net_a(40, 84))
    o.append(net_b(420, 84))

    # the data they both produce
    o.append(arrow((190, 312), (330, 372)))
    o.append(arrow((570, 312), (430, 372)))
    o.append(box(250, 382, 260, 128))
    o.append(caption((380, 406), "same quartet distribution"))
    o.append(quarnet(272, 414, s=0.82, labels=("1", "2", "3", "4")))
    o.append(quarnet(372, 414, s=0.82, labels=("1", "3", "2", "4")))
    o.append(label((380, 546), "identical data ⇒ not distinguishable", size=16,
                   color=RED, weight="600"))
    o.append(footer())
    write(os.path.join(RES, "theme-identifiability.svg"), "".join(o))


# --------------------------------------------------------------------------
# 3. DIVERSITY: which taxa to save (PD on a network)
# --------------------------------------------------------------------------
def fig_diversity():
    o = [header(W, H)]
    o.append(caption((W / 2, 26), "phylogenetic diversity: which taxa to protect?"))

    root = (380, 66)
    a, b = (238, 132), (522, 132)
    c, d = (168, 220), (312, 220)
    e, f = (452, 220), (594, 220)
    r1 = (380, 286)
    leaves = [(120, 350), (216, 350), (296, 350), (380, 366),
              (466, 350), (546, 350), (642, 350)]
    o.append(edge(root, a)); o.append(edge(root, b))
    o.append(edge(a, c)); o.append(edge(a, d))
    o.append(edge(b, e)); o.append(edge(b, f))
    o.append(edge(c, leaves[0])); o.append(edge(c, leaves[1]))
    o.append(edge(d, leaves[2])); o.append(edge(e, leaves[4]))
    o.append(edge(f, leaves[5])); o.append(edge(f, leaves[6]))
    o.append(edge(r1, leaves[3]))
    o.append(retic(d, r1, bow=10)); o.append(retic(e, r1, bow=-10))
    for p in (root, a, b, c, d, e, f):
        o.append(node(p))
    o.append(rnode(r1))

    chosen = {0, 3, 5}
    for i, p in enumerate(leaves):
        if i in chosen:
            o.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="12" fill="none" '
                     f'stroke="{RED}" stroke-width="2.4"/>')
        o.append(dot(p))
        o.append(label((p[0], p[1] + 30), str(i + 1), size=15))

    o.append(label((380, 434), "budget: pick 3 taxa", size=17, weight="600"))
    o.append(label((380, 462), "→ maximise the evolutionary history kept",
                   size=16, color="#4a5560", weight="400"))
    o.append(f'<circle cx="286" cy="500" r="9" fill="none" stroke="{RED}" stroke-width="2.2"/>')
    o.append(label((304, 506), "= selected", size=15, anchor="start", color="#4a5560"))
    o.append(footer())
    write(os.path.join(RES, "theme-diversity.svg"), "".join(o))


# --------------------------------------------------------------------------
# 4. PARAMETERS: scanwidth / how tree-like is the network
# --------------------------------------------------------------------------
def fig_parameters():
    o = [header(W, H)]
    o.append(caption((W / 2, 26), "structural parameters: how tree-like is it?"))

    # Every internal node has degree 3 (the root has the usual degree 2), and the
    # single reticulation r has exactly two parents (d, e) and one child.
    root = (380, 62)
    a, b = (250, 130), (510, 130)
    c, d = (170, 210), (330, 210)
    e, f = (430, 210), (590, 210)
    r = (380, 300)
    leaves = [(104, 392), (212, 392), (318, 392), (380, 392),
              (442, 392), (548, 392), (656, 392)]

    o.append(edge(root, a)); o.append(edge(root, b))
    o.append(edge(a, c)); o.append(edge(a, d))
    o.append(edge(b, e)); o.append(edge(b, f))
    o.append(edge(c, leaves[0])); o.append(edge(c, leaves[1]))
    o.append(edge(d, leaves[2])); o.append(edge(e, leaves[4]))
    o.append(edge(f, leaves[5])); o.append(edge(f, leaves[6]))
    o.append(edge(r, leaves[3]))
    o.append(retic(d, r, bow=10)); o.append(retic(e, r, bow=-10))
    for p in (root, a, b, c, d, e, f):
        o.append(node(p))
    o.append(rnode(r))
    for p in leaves:
        o.append(dot(p))
    for p, t in zip(leaves, "1234567"):
        o.append(label((p[0], p[1] + 24), t, size=15))

    # A horizontal "scan" cut; here it crosses exactly the four edges a-c, a-d,
    # b-e and b-f, so the grey dots and the stated number agree.
    y = 170
    o.append(f'<line x1="80" y1="{y}" x2="664" y2="{y}" stroke="{GREY}" '
             f'stroke-width="2" stroke-dasharray="9,7"/>')
    o.append(label((674, y + 6), "cut", size=15, anchor="start", color=GREY))
    for x in (210, 290, 470, 550):
        o.append(f'<circle cx="{x}" cy="{y}" r="5.4" fill="{GREY}"/>')

    o.append(label((380, 470), "scanwidth = max edges crossed by any cut",
                   size=17, weight="600"))
    o.append(label((380, 498), "small parameter → fast exact algorithms",
                   size=16, color="#4a5560", weight="400"))
    o.append(label((380, 528), "here the cut crosses 4", size=15, color=GREY))
    o.append(footer())
    write(os.path.join(RES, "theme-parameters.svg"), "".join(o))


# --------------------------------------------------------------------------
# 5. PLAIN-LANGUAGE: tree vs network (uses the xiph orthogonal cladogram look)
# --------------------------------------------------------------------------
def fig_tree_vs_network():
    w, h = 900, 430
    o = [header(w, h)]
    o.append(label((228, 34), "a tree", size=20, weight="600"))
    o.append(label((672, 34), "a network", size=20, weight="600"))
    o.append(f'<line x1="450" y1="56" x2="450" y2="374" stroke="#cfd9e0" stroke-width="1.6"/>')

    # ---- left: pure branching tree, orthogonal (xiph style) ----
    def T(x, y):
        return (x, y)
    o.append(elbow(T(96, 96), T(160, 96)))
    o.append(f'<path d="M96,96 V300" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round"/>')
    o.append(elbow(T(96, 300), T(160, 300)))
    # upper split
    o.append(f'<path d="M160,96 V60 H300" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="M160,96 V140 H300" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    # lower split
    o.append(f'<path d="M160,300 V250 H300" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="M160,300 V344 H300" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    for p in ((160, 96), (160, 300), (96, 96)):
        o.append(node(p, r=4.6))
    for yy, nm in ((60, "A"), (140, "B"), (250, "C"), (344, "D")):
        o.append(dot((300, yy)))
        o.append(label((316, yy + 6), nm, size=17, anchor="start"))
    o.append(caption((228, 404), "lineages only ever split apart"))

    # ---- right: same, but two lineages merge (red dashed reticulation) ----
    o.append(f'<path d="M540,96 V300" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round"/>')
    o.append(elbow(T(540, 96), T(604, 96)))
    o.append(elbow(T(540, 300), T(604, 300)))
    o.append(f'<path d="M604,96 V60 H744" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="M604,96 V150" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round"/>')
    o.append(f'<path d="M604,300 V344 H744" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="M604,300 V254" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round"/>')
    # the merge: two red dashed arcs into one reticulation node
    ret = (700, 202)
    o.append(retic((604, 150), ret, bow=14))
    o.append(retic((604, 254), ret, bow=-14))
    o.append(f'<path d="M700,202 H744" fill="none" stroke="{BLACK}" stroke-width="{EW}" '
             f'stroke-linecap="round"/>')
    for p in ((540, 96), (604, 96), (604, 300)):
        o.append(node(p, r=4.6))
    o.append(rnode(ret, r=6.2))
    for yy, nm in ((60, "A"), (344, "D")):
        o.append(dot((744, yy)))
        o.append(label((760, yy + 6), nm, size=17, anchor="start"))
    o.append(dot((744, 202)))
    o.append(label((760, 208), "E", size=17, anchor="start"))
    o.append(label((760, 228), "(hybrid)", size=13, anchor="start", color=RED, weight="400"))
    o.append(caption((672, 404), "two lineages can also merge back together"))
    o.append(footer())
    write(os.path.join(IMG, "tree-vs-network.svg"), "".join(o))


if __name__ == "__main__":
    fig_reconstruction()
    fig_identifiability()
    fig_diversity()
    fig_parameters()
    fig_tree_vs_network()
