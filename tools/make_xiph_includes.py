#!/usr/bin/env python3
"""Prepare the supplied Xiphophorus SVGs for inlining on the research page.

The two figures are used verbatim -- geometry is untouched. Two mechanical
changes are needed to embed them in a page:

  1. ID namespacing. Both files use the same ids (clipPath104, path105, ...).
     Inlined together they would collide and the clip-paths would bind to the
     wrong element, so each file's ids get a per-file prefix.
  2. #000000 -> currentColor, so the black strokes/labels follow the CSS text
     colour and turn white in dark mode. The reticulation red (#da0000) is left
     exactly as it is.

Also drops the XML prolog and the width/height attributes so the figure scales
to its container (the viewBox is kept).
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
IMG = os.path.join(ROOT, "assets", "images")
OUT = os.path.join(ROOT, "_includes", "figs")


def process(src, dst, prefix):
    s = open(os.path.join(IMG, src)).read()

    # 1) namespace every id and every url(#...) reference
    ids = set(re.findall(r'id="([^"]+)"', s))
    for i in sorted(ids, key=len, reverse=True):
        s = s.replace(f'id="{i}"', f'id="{prefix}{i}"')
        s = s.replace(f'url(#{i})', f'url(#{prefix}{i})')

    # 2) black -> currentColor (keep #da0000 reticulation red untouched)
    s = s.replace("stroke:#000000", "stroke:currentColor")
    s = s.replace("fill:#000000", "fill:currentColor")

    # drop the XML prolog / editor comment
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s)
    s = re.sub(r"<!--.*?-->\s*", "", s, flags=re.S)

    # let CSS size it: remove width/height on the root <svg>, keep viewBox
    s = re.sub(r'(<svg\b[^>]*?)\s+width="[^"]*"', r"\1", s, count=1)
    s = re.sub(r'(<svg\b[^>]*?)\s+height="[^"]*"', r"\1", s, count=1)

    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, dst), "w").write(s)
    print("wrote _includes/figs/%s  (%d ids namespaced '%s')" % (dst, len(ids), prefix))


if __name__ == "__main__":
    process("xiph-tree.svg", "xiph-tree.svg", "t-")
    process("xiph-network.svg", "xiph-network.svg", "n-")
