#!/usr/bin/env python3
"""Layman tree-vs-network illustration for the Research page intro."""
import math
from PIL import Image, ImageDraw

W, H, S = 1500, 720, 4
GROUND = (241, 250, 252)
PRIM = (26, 92, 122)
MID = (74, 143, 168)
CORAL = (239, 111, 83)

im = Image.new("RGB", (W * S, H * S), GROUND)
d = ImageDraw.Draw(im)

def sc(p): return (p[0] * S, p[1] * S)
def line(p1, p2, color, w):
    d.line([sc(p1), sc(p2)], fill=color, width=int(w * S), joint="curve")
    for p in (p1, p2):
        x, y = sc(p); r = w * S / 2.0
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)
def curve(pts, color, w):
    d.line([sc(p) for p in pts], fill=color, width=int(w * S), joint="curve")
def node(p, color, r=17, w=5, fill=GROUND):
    x, y = sc(p); rr = r * S
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=fill, outline=color, width=int(w * S))
def quad(p0, p1, p2, n=24):
    return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0], (1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1])
            for t in [i/n for i in range(n+1)]]

# ---- LEFT: a phylogenetic tree (purely branching) ----
root = (375, 135)
i1, i2 = (250, 320), (500, 320)
l = [(175, 545), (325, 545), (430, 545), (580, 545)]
for a, b in [(root, i1), (root, i2), (i1, l[0]), (i1, l[1]), (i2, l[2]), (i2, l[3])]:
    line(a, b, PRIM, 7)
for p in (root, i1, i2) + tuple(l):
    node(p, PRIM)

# ---- divider ----
d.line([sc((750, 90)), sc((750, 630))], fill=(206, 218, 226), width=int(2 * S))

# ---- RIGHT: a phylogenetic network (with a reticulation / merge) ----
root2 = (1130, 135)
a2, b2 = (990, 320), (1270, 320)
ret = (1130, 445)
la, lm, lb = (915, 560), (1130, 565), (1345, 560)
line(root2, a2, PRIM, 7); line(root2, b2, PRIM, 7)
line(a2, la, PRIM, 7); line(b2, lb, PRIM, 7)
line(ret, lm, PRIM, 7)
# reticulation: two lineages merging (coral)
curve(quad(a2, (1045, 385), ret), CORAL, 9)
curve(quad(b2, (1215, 385), ret), CORAL, 9)
for p in (root2, a2, b2, la, lm, lb):
    node(p, PRIM)
node(ret, CORAL, fill=CORAL)

out = "/home/nholtgreve/Documents/Code/nielsholtgrefe.github.io/assets/images/tree-vs-network.png"
im.resize((W, H), Image.LANCZOS).save(out)
print("wrote", out)
