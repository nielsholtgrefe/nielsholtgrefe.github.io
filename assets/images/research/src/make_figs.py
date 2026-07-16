#!/usr/bin/env python3
"""Research-page figures, drawn to match Niels' own originals.

  theme-reconstruction.svg  fig2 pipeline: MSA -> quarnets -> semi-directed net
  theme-identifiability.svg two distinct nets, same displayed quartets
  theme-diversity.svg       budgeted taxon choice on a network
  theme-parameters.svg      the scanwidth TikZ: rooted DAG + graded red cut arcs
  tree-vs-network.svg       Xiphophorus tree vs the real Xiphophorus network
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


# ==========================================================================
# fig2-style quarnet: 4 leaves, one reticulation, red dashed arcs
# ==========================================================================
def quarnet(ox, oy, s=1.0, labels=("1", "2", "3", "4")):
    """Binary 4-leaf semi-directed network (verified by check_binary.py).

    root -> a,b ; a -> l1, r ; b -> l4, r ; r -> m ; m -> l2, l3.
    Degrees: root 2; a, b, r, m all 3; leaves 1.
    """
    def P(x, y):
        return (ox + x * s, oy + y * s)
    top, a, b = P(50, 4), P(20, 36), P(80, 36)
    r = P(50, 62)
    m = P(50, 80)
    l1, l4 = P(2, 72), P(98, 72)
    l2, l3 = P(30, 100), P(70, 100)
    out = [edge(top, a), edge(top, b), edge(a, l1), edge(b, l4),
           edge(r, m), edge(m, l2), edge(m, l3),
           retic(a, r, bow=7 * s), retic(b, r, bow=-7 * s)]
    for p in (top, a, b, m):
        out.append(node(p, r=3.6 * s))
    out.append(rnode(r, r=4.2 * s))
    for p in (l1, l2, l3, l4):
        out.append(dot(p, r=3.4 * s))
    for p, t in zip((l1, l2, l3, l4), labels):
        dx = -8.5 * s if p[0] < ox + 50 * s else 8.5 * s
        out.append(label((p[0] + dx, p[1] + 4.5 * s), t, size=12.5 * s))
    return "".join(out)


# ==========================================================================
# 1. RECONSTRUCTION  (mirrors his fig2 pipeline)
# ==========================================================================
def fig_reconstruction():
    o = [header(W, H)]
    o.append(caption((W / 2, 24), "from sequences to a semi-directed network"))

    o.append(box(24, 42, 176, 134))
    for i, s in enumerate(["-GCG-CACT", "AGCG-C-CT", "-GCCA-AGT",
                           "GCCAA-ATT", "-CGT-ATCT"]):
        o.append(f'<text x="36" y="{72 + i*22}" font-size="15" fill="{BLACK}" '
                 f'font-family="DejaVu Sans Mono, Menlo, monospace">{s}</text>')
    o.append(caption((112, 194), "multiple sequence alignment"))

    o.append(box(246, 42, 250, 134))
    o.append(quarnet(258, 62, s=0.86, labels=("1", "2", "3", "4")))
    o.append(quarnet(374, 62, s=0.86, labels=("2", "3", "5", "6")))
    o.append(caption((371, 194), "dense set of quarnets"))

    o.append(arrow((208, 108), (240, 108)))
    o.append(arrow((504, 108), (536, 108)))

    o.append(box(546, 42, 190, 134))
    o.append(quarnet(568, 58, s=1.0, labels=("1", "2", "3", "4")))
    o.append(caption((641, 194), "puzzle them together"))

    root = (380, 238)
    a, b = (250, 296), (510, 296)
    c, d = (190, 372), (322, 372)
    e, f = (438, 372), (572, 372)
    r1 = (380, 428)
    lv = [(150, 474), (232, 474), (300, 474), (380, 496),
          (462, 474), (530, 474), (612, 474)]
    o += [edge(root, a), edge(root, b), edge(a, c), edge(a, d),
          edge(b, e), edge(b, f), edge(c, lv[0]), edge(c, lv[1]),
          edge(d, lv[2]), edge(e, lv[4]), edge(f, lv[5]), edge(f, lv[6]),
          edge(r1, lv[3]), retic(d, r1, bow=10), retic(e, r1, bow=-10)]
    for p in (root, a, b, c, d, e, f):
        o.append(node(p))
    o.append(rnode(r1))
    for p, t in zip(lv, "1234567"):
        o.append(dot(p)); o.append(label((p[0], p[1] + 22), t, size=14))
    o.append(caption((380, 540), "reconstructed semi-directed network"))
    o.append(footer())
    write(os.path.join(RES, "theme-reconstruction.svg"), "".join(o))


# ==========================================================================
# 2. IDENTIFIABILITY
# ==========================================================================
def fig_identifiability():
    o = [header(W, H)]
    o.append(caption((W / 2, 24), "can the data tell two networks apart?"))

    o.append(box(30, 44, 320, 252))
    o.append(box(410, 44, 320, 252))
    o.append(label((190, 72), "network A", size=15))
    o.append(label((570, 72), "network B", size=15))

    def net_a(ox, oy):
        """Symmetric 4-cycle. root->a,b; a->l1,r; b->l4,r; r->m; m->l2,l3."""
        def P(x, y):
            return (ox + x, oy + y)
        top, a, b = P(150, 18), P(62, 66), P(238, 66)
        r, m = P(150, 118), P(150, 152)
        l1, l4 = P(18, 186), P(282, 186)
        l2, l3 = P(112, 186), P(188, 186)
        out = [edge(top, a), edge(top, b), edge(a, l1), edge(b, l4),
               edge(r, m), edge(m, l2), edge(m, l3),
               retic(a, r, bow=12), retic(b, r, bow=-12)]
        for p in (top, a, b, m):
            out.append(node(p))
        out.append(rnode(r))
        for p, t in zip((l1, l2, l3, l4), ("1", "2", "3", "4")):
            out.append(dot(p)); out.append(label((p[0], p[1] + 21), t, size=14))
        return "".join(out)

    def net_b(ox, oy):
        """Skewed cycle: root->a,c; a->l1,r; c->l4,g; g->l3,r; r->l2."""
        def P(x, y):
            return (ox + x, oy + y)
        top, a, c = P(150, 18), P(70, 66), P(232, 66)
        g = P(186, 122)
        r = P(104, 140)
        l1, l4 = P(18, 186), P(282, 186)
        l3, l2 = P(210, 186), P(104, 186)
        out = [edge(top, a), edge(top, c), edge(a, l1), edge(c, l4),
               edge(c, g), edge(g, l3), edge(r, l2),
               retic(a, r, bow=10), retic(g, r, bow=-18)]
        for p in (top, a, c, g):
            out.append(node(p))
        out.append(rnode(r))
        for p, t in zip((l1, l2, l3, l4), ("1", "2", "3", "4")):
            out.append(dot(p)); out.append(label((p[0], p[1] + 21), t, size=14))
        return "".join(out)

    o.append(net_a(40, 82)); o.append(net_b(420, 82))
    o.append(arrow((190, 312), (330, 374)))
    o.append(arrow((570, 312), (430, 374)))
    o.append(box(250, 384, 260, 126))
    o.append(caption((380, 408), "same displayed quartets"))
    o.append(quarnet(272, 416, s=0.80, labels=("1", "2", "3", "4")))
    o.append(quarnet(372, 416, s=0.80, labels=("1", "3", "2", "4")))
    o.append(label((380, 546), "identical data ⇒ not distinguishable",
                   size=15, color=RED, weight="600"))
    o.append(footer())
    write(os.path.join(RES, "theme-identifiability.svg"), "".join(o))


# ==========================================================================
# 3. DIVERSITY
# ==========================================================================
def fig_diversity():
    o = [header(W, H)]
    o.append(caption((W / 2, 24), "which taxa preserve the most diversity?"))

    root = (380, 70)
    a, b = (238, 136), (522, 136)
    c, d = (168, 222), (312, 222)
    e, f = (452, 222), (594, 222)
    r1 = (380, 288)
    lv = [(120, 352), (216, 352), (296, 352), (380, 368),
          (466, 352), (546, 352), (642, 352)]
    o += [edge(root, a), edge(root, b), edge(a, c), edge(a, d),
          edge(b, e), edge(b, f), edge(c, lv[0]), edge(c, lv[1]),
          edge(d, lv[2]), edge(e, lv[4]), edge(f, lv[5]), edge(f, lv[6]),
          edge(r1, lv[3]), retic(d, r1, bow=10), retic(e, r1, bow=-10)]
    for p in (root, a, b, c, d, e, f):
        o.append(node(p))
    o.append(rnode(r1))
    chosen = {0, 3, 5}
    for i, p in enumerate(lv):
        if i in chosen:
            o.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="11.5" fill="none" '
                     f'stroke="{RED}" stroke-width="2.2"/>')
        o.append(dot(p)); o.append(label((p[0], p[1] + 30), str(i + 1), size=14))
    o.append(label((380, 440), "budget: protect 3 taxa", size=16, weight="600"))
    o.append(caption((380, 468), "maximise the evolutionary history kept", size=15))
    o.append(f'<circle cx="292" cy="504" r="8.5" fill="none" stroke="{RED}" '
             f'stroke-width="2.2"/>')
    o.append(label((308, 509), "= selected", size=14, anchor="start", color="#3f4a54"))
    o.append(footer())
    write(os.path.join(RES, "theme-diversity.svg"), "".join(o))


# ==========================================================================
# 4. PARAMETERS — a faithful redraw of his scanwidth TikZ
#    rooted DAG, curved arcs, and a family of red cut-arcs graded 17%..100%
# ==========================================================================
def fig_parameters():
    o = [header(W, H)]
    o.append(caption((W / 2, 24), "scanwidth: how tree-like is the network?"))

    # TikZ coords (x right, y UP) -> svg (y down).
    # x in [0.5, 8]  -> [96, 664]   |  y in [2, 8.5] -> [452, 84]
    SX, SY = 568.0 / 7.5, 368.0 / 6.5

    def P(x, y):
        return (96.0 + (x - 0.5) * SX, 452.0 - (y - 2.0) * SY)

    rho = P(5, 8.5); w_ = P(6.5, 7.5); q = P(5, 6.5); v = P(3.5, 5.5)
    u = P(2, 4.5);   y_ = P(5, 4.5);   x_ = P(3.5, 3.5)
    a = P(0.5, 3.5); b = P(3.5, 2);    c = P(6.5, 3.5); d = P(8, 6.5)

    # --- DAG edges, curved exactly where his TikZ bends ---
    o.append(curve(rho, q, bow=-78))        # bend left 45, looseness 2.5
    o.append(edge(rho, w_))
    o.append(edge(w_, d))
    o.append(curve(w_, y_, bow=-70))        # in=135, out=-120, looseness 2.25
    o.append(curve(q, u, bow=16))           # bend right 15
    o.append(edge(q, v))
    o.append(edge(u, a))
    o.append(edge(u, x_))
    o.append(curve(v, x_, bow=60))          # bend right 45, looseness 2.5
    o.append(edge(v, y_))
    o.append(edge(y_, c))
    o.append(edge(x_, b))

    # --- the graded red cut arcs (his red!17 .. red!100) ---
    def A(x, y):
        return P(x, y)
    cuts = [
        (A(0.75, 4.5), A(1.5, 3.25), 0.17),
        (A(2.75, 2.75), A(4.25, 2.75), 0.17),
        (A(5.25, 3.5), A(6.25, 4.5), 0.17),
        (A(2.25, 3.5), A(3.5, 4.5), 0.34),
        (A(3.0, 4.5), A(2.0, 5.5), 0.50),
        (A(3.75, 4.5), A(5.0, 5.25), 0.34),
        (A(4.75, 5.5), A(3.75, 6.5), 0.67),
        (A(5.0, 7.5), A(6.0, 6.5), 0.82),
        (A(6.75, 6.5), A(7.75, 7.5), 0.17),
        (A(5.25, 7.5), A(6.25, 8.5), 1.00),
    ]
    for p, qq, sh in cuts:
        o.append(cut_arc(p, qq, sh, bow=10, w=4.2))

    # --- nodes: reticulations (indegree 2) are x and y ---
    for p in (rho, w_, q, v, u):
        o.append(node(p))
    o.append(rnode(x_)); o.append(rnode(y_))
    for p in (a, b, c, d):
        o.append(dot(p))

    for p, t, dx, dy in ((rho, "ρ", 14, -6), (w_, "w", 14, -6), (q, "q", -14, -6),
                         (v, "v", -14, -6), (u, "u", -14, -6), (y_, "y", 14, -4),
                         (x_, "x", 14, 4), (a, "a", 0, 20), (b, "b", 0, 20),
                         (c, "c", 0, 20), (d, "d", 0, 20)):
        o.append(label((p[0] + dx, p[1] + dy), f"<tspan font-style='italic'>{t}</tspan>",
                       size=15))

    o.append(caption((W / 2, 500), "each red arc is a cut; darker = more edges crossed",
                     size=15))
    o.append(label((W / 2, 530), "scanwidth = the darkest cut",
                   size=16, weight="600"))
    o.append(footer())
    write(os.path.join(RES, "theme-parameters.svg"), "".join(o))


# ==========================================================================
# 5. TREE vs NETWORK — the real Xiphophorus example, xiph-style orthogonal
# ==========================================================================
SPECIES = ["X.continens", "X.pygmaeus", "X.nigrensis", "X.multilineatus",
           "X.montezumae", "X.nezahualcoyotl", "X.cortezi", "X.malinche",
           "X.birchmanni"]


def xiph(ox, oy, with_retics):
    """Orthogonal Xiphophorus cladogram; optionally with the two reticulations."""
    LX = ox + 250                      # leaf tips (right-aligned, as in xiph)
    ys = [oy + 20 + i * 34 for i in range(9)]
    out = []

    # internal x positions (deeper = further left)
    x0 = ox + 18     # root spine
    x1 = ox + 52
    x2 = ox + 92
    x3 = ox + 132
    x4 = ox + 172

    def leaf(i, fromx, fromy):
        out.append(elbow_hv((fromx, fromy), (LX, ys[i])))
        out.append(dot((LX, ys[i]), r=3.4))
        out.append(label((LX + 9, ys[i] + 4.5), SPECIES[i], size=12.5,
                         anchor="start", italic=True))

    # ---- northern-swordtail style backbone ----
    # split: (continens,pygmaeus,nigrensis,multilineatus) | (rest)
    yA = (ys[0] + ys[3]) / 2
    yB = (ys[4] + ys[8]) / 2
    out.append(f'<path d="M{x0},{yA} V{yB}" fill="none" stroke="{BLACK}" '
               f'stroke-width="{EW}" stroke-linecap="round"/>')
    out.append(elbow_hv((x0, yA), (x1, yA)))
    out.append(elbow_hv((x0, yB), (x1, yB)))

    # upper clade
    yA1 = (ys[0] + ys[1]) / 2
    yA2 = (ys[2] + ys[3]) / 2
    out.append(f'<path d="M{x1},{yA1} V{yA2}" fill="none" stroke="{BLACK}" '
               f'stroke-width="{EW}" stroke-linecap="round"/>')
    out.append(elbow_hv((x1, yA1), (x2, yA1)))
    out.append(elbow_hv((x1, yA2), (x2, yA2)))
    leaf(0, x2, ys[0]); leaf(1, x2, ys[1])
    leaf(2, x2, ys[2]); leaf(3, x2, ys[3])
    out.append(f'<path d="M{x2},{ys[0]} V{ys[1]}" fill="none" stroke="{BLACK}" '
               f'stroke-width="{EW}" stroke-linecap="round"/>')
    out.append(f'<path d="M{x2},{ys[2]} V{ys[3]}" fill="none" stroke="{BLACK}" '
               f'stroke-width="{EW}" stroke-linecap="round"/>')

    # lower clade: (montezumae,nezahualcoyotl) (cortezi) (malinche,birchmanni)
    yB1 = (ys[4] + ys[5]) / 2
    yB2 = (ys[7] + ys[8]) / 2
    out.append(f'<path d="M{x1},{yB1} V{yB2}" fill="none" stroke="{BLACK}" '
               f'stroke-width="{EW}" stroke-linecap="round"/>')
    out.append(elbow_hv((x1, yB1), (x2, yB1)))
    out.append(elbow_hv((x1, yB2), (x2, yB2)))
    out.append(f'<path d="M{x2},{ys[4]} V{ys[5]}" fill="none" stroke="{BLACK}" '
               f'stroke-width="{EW}" stroke-linecap="round"/>')
    leaf(4, x2, ys[4]); leaf(5, x2, ys[5])
    out.append(f'<path d="M{x2},{ys[7]} V{ys[8]}" fill="none" stroke="{BLACK}" '
               f'stroke-width="{EW}" stroke-linecap="round"/>')
    leaf(7, x2, ys[7]); leaf(8, x2, ys[8])
    # cortezi hangs off the lower spine
    out.append(elbow_hv((x1, (yB1 + yB2) / 2), (x3, ys[6])))
    leaf(6, x3, ys[6])

    if with_retics:
        # (1) into the pygmaeus / nigrensis region
        out.append(retic((x2, ys[1] - 10), (x3 + 6, ys[2] - 2), bow=-14))
        out.append(rnode((x3 + 6, ys[2] - 2), r=4.4))
        # (2) into X.cortezi, from the montezumae side and the malinche side
        out.append(retic((x2 + 10, ys[5]), (x3 - 4, ys[6] - 3), bow=-10))
        out.append(retic((x2 + 10, ys[7]), (x3 - 4, ys[6] + 3), bow=10))
        out.append(rnode((x3 - 4, ys[6]), r=4.4))
    return "".join(out)


def fig_tree_vs_network():
    w, h = 960, 400
    o = [header(w, h)]
    o.append(label((236, 30), "a tree", size=19, weight="600"))
    o.append(label((716, 30), "a network", size=19, weight="600"))
    o.append(f'<line x1="474" y1="44" x2="474" y2="352" stroke="#cfd9e0" '
             f'stroke-width="1.4"/>')
    o.append(xiph(30, 44, with_retics=False))
    o.append(xiph(510, 44, with_retics=True))
    o.append(caption((236, 384), "lineages only ever split apart"))
    o.append(caption((716, 384), "two lineages can also merge back together"))
    o.append(footer())
    write(os.path.join(IMG, "tree-vs-network.svg"), "".join(o))


if __name__ == "__main__":
    fig_reconstruction()
    fig_identifiability()
    fig_diversity()
    fig_parameters()
    fig_tree_vs_network()
