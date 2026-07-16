#!/usr/bin/env python3
"""Assert every network drawn on the research page is BINARY.

Binary phylogenetic network:
  * every node has degree <= 3
  * leaves          degree 1
  * the root        degree 2
  * tree nodes      degree 3 (1 parent, 2 children)
  * reticulations   degree 3 (2 parents, 1 child)   <- the easy one to get wrong
Run this after editing make_figs.py.
"""

NETS = {
    # --- quarnet used inside the reconstruction + identifiability boxes ---
    # A binary 4-leaf quarnet: root -> a,b ; a -> l1, r ; b -> l4, r ;
    # r -> m ; m -> l2, l3.  Every node degree <= 3.
    "quarnet": dict(
        root="top",
        edges=[("top", "a"), ("top", "b"),
               ("a", "l1"), ("b", "l4"),
               ("r", "m"), ("m", "l2"), ("m", "l3")],
        retic=[("a", "r"), ("b", "r")],
    ),
    # --- big network in reconstruction + diversity ---
    "reconstruction/diversity": dict(
        root="root",
        edges=[("root", "a"), ("root", "b"), ("a", "c"), ("a", "d"),
               ("b", "e"), ("b", "f"), ("c", "L1"), ("c", "L2"),
               ("d", "L3"), ("e", "L5"), ("f", "L6"), ("f", "L7"),
               ("r", "L4")],
        retic=[("d", "r"), ("e", "r")],
    ),
    "identifiability A": dict(
        root="top",
        edges=[("top", "a"), ("top", "b"),
               ("a", "l1"), ("b", "l4"),
               ("r", "m"), ("m", "l2"), ("m", "l3")],
        retic=[("a", "r"), ("b", "r")],
    ),
    # B: same leaves, genuinely different shape. The cycle is skewed: one
    # parent of r is a, the other is g (a child of c), and l3 hangs off c.
    # root=2, a=3, c=3, g=3, r=3 -> binary.
    "identifiability B": dict(
        root="top",
        edges=[("top", "a"), ("top", "c"),
               ("a", "l1"), ("c", "l4"), ("c", "g"), ("g", "l3"),
               ("r", "l2")],
        retic=[("a", "r"), ("g", "r")],
    ),
    # --- the scanwidth DAG, transcribed from his TikZ ---
    "parameters/scanwidth": dict(
        root="rho",
        edges=[("rho", "q"), ("rho", "w"), ("w", "d"), ("w", "y"),
               ("q", "u"), ("q", "v"), ("u", "a"), ("u", "x"),
               ("v", "y"), ("y", "c"), ("x", "b")],
        retic=[("u", "x"), ("v", "x")],
    ),
}


def check(name, spec):
    E = list(spec["edges"]) + list(spec["retic"])
    E = list(dict.fromkeys(E))                      # de-dup
    deg, indeg = {}, {}
    for u, v in E:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
        indeg[v] = indeg.get(v, 0) + 1
        indeg.setdefault(u, indeg.get(u, 0))
    problems = []
    for n, d in sorted(deg.items()):
        if d > 3:
            problems.append(f"{n}: degree {d} (>3, not binary)")
    for n, i in sorted(indeg.items()):
        if i > 2:
            problems.append(f"{n}: indegree {i} (>2)")
    rets = sorted([n for n, i in indeg.items() if i == 2])
    for r in rets:
        out = sum(1 for u, v in E if u == r)
        if out != 1:
            problems.append(f"reticulation {r}: {out} children (must be exactly 1)")
    root = spec["root"]
    if deg.get(root) != 2:
        problems.append(f"root {root}: degree {deg.get(root)} (expected 2)")
    ok = not problems
    print(f"{name:26s} maxdeg={max(deg.values())}  retics={rets}  "
          f"{'BINARY OK' if ok else 'FAIL'}")
    for p in problems:
        print("      -", p)
    return ok


if __name__ == "__main__":
    allok = all(check(n, s) for n, s in NETS.items())
    print()
    print("ALL NETWORKS BINARY" if allok else "SOME NETWORKS ARE NOT BINARY")
    raise SystemExit(0 if allok else 1)
