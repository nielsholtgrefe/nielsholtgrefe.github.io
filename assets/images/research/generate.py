#!/usr/bin/env python3
"""Blueprint research figures -> flat vector-style PNGs (supersampled)."""
import math
from PIL import Image, ImageDraw

W, H, S = 1600, 1200, 4
GROUND = (241, 250, 252)   # #F1FAFC
PRIM   = (26, 92, 122)     # #1a5c7a
MID    = (74, 143, 168)    # #4a8fa8
CORAL  = (239, 111, 83)    # #EF6F53

def blend(c1, c2, t):
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))

GHOST = blend(CORAL, GROUND, 0.72)     # faint coral (ghost sweep)
FAINT = blend(MID, GROUND, 0.55)       # faint teal (brackets/guides)

class Fig:
    def __init__(self):
        self.im = Image.new("RGB", (W * S, H * S), GROUND)
        self.d = ImageDraw.Draw(self.im)
    def sc(self, p): return (p[0] * S, p[1] * S)
    def line(self, p1, p2, color, w, cap=True):
        self.d.line([self.sc(p1), self.sc(p2)], fill=color, width=int(w * S), joint="curve")
        if cap:
            self._cap(p1, color, w); self._cap(p2, color, w)
    def curve(self, pts, color, w, cap=True):
        self.d.line([self.sc(p) for p in pts], fill=color, width=int(w * S), joint="curve")
        if cap:
            self._cap(pts[0], color, w); self._cap(pts[-1], color, w)
    def _cap(self, p, color, w):
        x, y = self.sc(p); r = w * S / 2.0
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    def node(self, p, color, r=17, w=5, fill=GROUND):
        x, y = self.sc(p); rr = r * S
        self.d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=fill, outline=color, width=int(w * S))
    def dot(self, p, color, r=8):
        x, y = self.sc(p); rr = r * S
        self.d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color)
    def arrow(self, p1, p2, color, w, r=17, head=22, hw=11):
        # straight edge p1->p2 with a triangular arrowhead just outside child node p2
        self.line(p1, p2, color, w)
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        tip = (p2[0] - ux * (r + 3), p2[1] - uy * (r + 3))
        base = (tip[0] - ux * head, tip[1] - uy * head)
        px, py = -uy, ux
        a = (base[0] + px * hw, base[1] + py * hw)
        b = (base[0] - px * hw, base[1] - py * hw)
        self.d.polygon([self.sc(tip), self.sc(a), self.sc(b)], fill=color)
    def save(self, path):
        self.im.resize((W, H), Image.LANCZOS).save(path)

def quad(p0, p1, p2, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts

OUT = "/home/nholtgreve/Documents/Code/nielsholtgrefe.github.io/assets/images/research/"

# ---------------------------------------------------------------- FIG 1: RECONSTRUCTION
def fig_reconstruction():
    f = Fig()
    # --- three small quarnet fragments, upper-left, distinct with light overlap ---
    def quarnet(cx, cy, r=10):
        p, q = (cx - 30, cy), (cx + 30, cy)
        f.line(p, q, MID, 5)
        leaves = [(cx - 82, cy - 54), (cx - 82, cy + 54), (cx + 82, cy - 54), (cx + 82, cy + 54)]
        f.line(p, leaves[0], MID, 5); f.line(p, leaves[1], MID, 5)
        f.line(q, leaves[2], MID, 5); f.line(q, leaves[3], MID, 5)
        for lp in leaves: f.node(lp, MID, r=r, w=4)
        f.node(p, MID, r=r, w=4); f.node(q, MID, r=r, w=4)
    quarnet(280, 235); quarnet(500, 315); quarnet(335, 500)
    # --- assembly guide arrow rightward ---
    f.arrow((590, 430), (770, 470), FAINT, 5, r=0, head=26, hw=13)
    # --- assembled reticulated network on the right ---
    root = (1080, 215)
    a, b = (930, 400), (1230, 400)
    ret = (1080, 585)
    la, lm, lb = (870, 800), (1080, 820), (1290, 800)
    f.arrow(root, a, PRIM, 7); f.arrow(root, b, PRIM, 7)
    # reticulation arcs (coral hero): a->ret and b->ret curved, meeting at ret
    f.curve(quad(a, (985, 520), ret), CORAL, 9)
    f.curve(quad(b, (1175, 520), ret), CORAL, 9)
    f.arrow(a, la, PRIM, 7); f.arrow(b, lb, PRIM, 7); f.arrow(ret, lm, PRIM, 7)
    for p in (root, a, b, la, lm, lb): f.node(p, PRIM)
    f.node(ret, CORAL, fill=CORAL)
    f.save(OUT + "theme-reconstruction.png")

# ---------------------------------------------------------------- FIG 2: IDENTIFIABILITY
def fig_identifiability():
    f = Fig()
    def net(cx, coral_side):
        root = (cx, 300)
        a, b = (cx - 135, 470), (cx + 135, 470)
        ret = (cx, 630)
        la, lm, lb = (cx - 175, 800), (cx, 810), (cx + 175, 800)
        f.arrow(root, a, PRIM, 7); f.arrow(root, b, PRIM, 7)
        # reticulation edges into ret; the "differing" one is coral
        left_col = CORAL if coral_side == "L" else PRIM
        right_col = CORAL if coral_side == "R" else PRIM
        f.curve(quad(a, (cx - 70, 555), ret), left_col, 9 if left_col == CORAL else 7)
        f.curve(quad(b, (cx + 70, 555), ret), right_col, 9 if right_col == CORAL else 7)
        f.arrow(a, la, PRIM, 7); f.arrow(b, lb, PRIM, 7); f.arrow(ret, lm, PRIM, 7)
        for p in (root, a, b, ret, la, lm, lb): f.node(p, PRIM)
    net(470, "L")
    net(1130, "R")
    # central compare mark: two coral dots joined by a short link
    f.line((800, 520), (800, 600), CORAL, 9)
    f.dot((800, 520), CORAL, r=15); f.dot((800, 600), CORAL, r=15)
    f.save(OUT + "theme-identifiability.png")

# ---------------------------------------------------------------- FIG 3: DIVERSITY
def fig_diversity():
    f = Fig()
    root = (800, 210)
    i1, i2 = (560, 400), (1040, 400)
    j1, j2, j3, j4 = (430, 610), (735, 610), (900, 610), (1170, 610)
    leaves = [(360, 830), (500, 830), (660, 830), (800, 830),
              (940, 830), (1090, 830), (1240, 830)]
    # context tree in mid teal
    ctx = [(root, i1), (root, i2), (i1, j1), (i1, j2), (i2, j3), (i2, j4),
           (i2, j2),  # reticulation: j2 has parents i1 and i2
           (j1, leaves[0]), (j1, leaves[1]), (j2, leaves[2]), (j2, leaves[3]),
           (j3, leaves[4]), (j3, leaves[5]), (j4, leaves[6])]
    for p1, p2 in ctx: f.line(p1, p2, MID, 5)
    # chosen coral subset: leaves[1], leaves[3], leaves[6] and their paths to root
    coral_edges = [(root, i1), (i1, j1), (j1, leaves[1]),
                   (root, i1), (i1, j2), (j2, leaves[3]),
                   (root, i2), (i2, j4), (j4, leaves[6])]
    for p1, p2 in coral_edges: f.line(p1, p2, CORAL, 7)
    # faint bracket under the leaf row (budget)
    by = 930
    f.line((360, by), (1240, by), FAINT, 4, cap=False)
    f.line((360, by), (360, by - 22), FAINT, 4, cap=False)
    f.line((1240, by), (1240, by - 22), FAINT, 4, cap=False)
    f.line((800, by), (800, by + 22), FAINT, 4, cap=False)
    # nodes: context mid, chosen leaves coral-filled
    for p in (root, i1, i2, j1, j2, j3, j4): f.node(p, MID)
    chosen = {1, 3, 6}
    for idx, p in enumerate(leaves):
        if idx in chosen: f.node(p, CORAL, fill=CORAL)
        else: f.node(p, MID)
    f.save(OUT + "theme-diversity.png")

# ---------------------------------------------------------------- FIG 4: PARAMETERS
def fig_parameters():
    f = Fig()
    s = (720, 235)
    a, b = (540, 445), (930, 445)
    c, dd, e = (430, 660), (735, 660), (1055, 660)
    g, h = (585, 875), (915, 875)
    edges = [(s, a), (s, b), (a, c), (a, dd), (b, dd), (b, e),
             (c, g), (dd, g), (dd, h), (e, h)]
    for p1, p2 in edges: f.arrow(p1, p2, PRIM, 7)
    def xcross(p1, p2, x):
        if (p1[0] - x) * (p2[0] - x) > 0: return None
        t = (x - p1[0]) / (p2[0] - p1[0])
        return (x, p1[1] + t * (p2[1] - p1[1]))
    # ghost sweep (faint), a prior step to the left, with faint intersection dots
    ghost_x = 610
    f.line((ghost_x, 175), (ghost_x, 1000), GHOST, 7, cap=False)
    for p1, p2 in edges:
        pt = xcross(p1, p2, ghost_x)
        if pt: f.dot(pt, GHOST, r=11)
    # coral sweep line + intersection dots (the current cut width)
    sweep_x = 822
    f.line((sweep_x, 165), (sweep_x, 1010), CORAL, 9, cap=False)
    for p1, p2 in edges:
        pt = xcross(p1, p2, sweep_x)
        if pt: f.dot(pt, CORAL, r=13)
    for p in (s, a, b, c, dd, e, g, h): f.node(p, PRIM)
    f.save(OUT + "theme-parameters.png")

fig_reconstruction()
fig_identifiability()
fig_diversity()
fig_parameters()
print("done: 4 figures written to", OUT)
