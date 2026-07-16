"""Drawing helpers in Niels' own figure style.

Conventions taken from his fig2.svg / xiph0.svg (see conventions.txt):
  - tree edges      : solid black, thin
  - reticulation    : RED dashed, with a filled arrowhead pointing INTO the
                      reticulation node (the semi-directed convention)
  - internal node   : hollow (white fill, black stroke)
  - reticulation    : filled node
  - leaves          : filled dots with plain numeric labels
  - captions        : italic sans-serif
Everything is emitted as plain SVG so it stays crisp at any size and can be
recoloured by CSS-free means (the site shows them inside a light figure box).
"""

BLACK = "#111111"
RED = "#d81f1f"
GREY = "#8a949b"

# stroke widths tuned for a ~760x570 viewBox
EW = 2.2          # tree edge width
RW = 2.6          # reticulation edge width
DASH = "7,4.6"    # red dash pattern (same ratio as his 3.985,2.657)


def header(w, h):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="Inter, Helvetica, Arial, sans-serif">'
        f'<defs>'
        f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" '
        f'markerHeight="5.5" orient="auto-start-reverse">'
        f'<path d="M0,1.6 L9,5 L0,8.4 z" fill="{RED}"/></marker>'
        f'<marker id="arb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" '
        f'markerHeight="5.5" orient="auto-start-reverse">'
        f'<path d="M0,1.6 L9,5 L0,8.4 z" fill="{BLACK}"/></marker>'
        f'</defs><rect width="{w}" height="{h}" fill="none"/>'
    )


def footer():
    return "</svg>"


def edge(p, q, w=EW, color=BLACK):
    """Solid tree edge."""
    return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')


def elbow(p, q, w=EW, color=BLACK):
    """Orthogonal elbow (xiph cladogram style): vertical then horizontal."""
    return (f'<path d="M{p[0]:.1f},{p[1]:.1f} V{q[1]:.1f} H{q[0]:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')


def retic(p, q, bow=0.0, w=RW, arrow=True):
    """Red dashed reticulation arc p -> q, optionally bowed, arrowhead at q."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = max((dx * dx + dy * dy) ** 0.5, 1e-6)
    cx, cy = mx - dy / L * bow, my + dx / L * bow
    a = ' marker-end="url(#ar)"' if arrow else ""
    return (f'<path d="M{p[0]:.1f},{p[1]:.1f} Q{cx:.1f},{cy:.1f} {q[0]:.1f},{q[1]:.1f}" '
            f'fill="none" stroke="{RED}" stroke-width="{w}" stroke-dasharray="{DASH}" '
            f'stroke-linecap="round"{a}/>')


def arrow(p, q, w=2.6, color=BLACK):
    return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'marker-end="url(#arb)"/>')


def node(p, r=5.0, fill="#ffffff"):
    """Hollow internal node."""
    return (f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{BLACK}" stroke-width="{EW}"/>')


def dot(p, r=4.6, color=BLACK):
    """Filled node (leaf, or the reticulation vertex)."""
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{color}"/>'


def rnode(p, r=5.6):
    """Reticulation vertex: filled, red."""
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{RED}"/>'


def label(p, s, size=17, anchor="middle", italic=False, color=BLACK, weight="500"):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{p[0]:.1f}" y="{p[1]:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{st}>{s}</text>')


def caption(p, s, size=16):
    return label(p, s, size=size, italic=True, color="#4a5560", weight="400")


def box(x, y, w, h, r=7, color="#b9c6cf"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}" '
            f'fill="none" stroke="{color}" stroke-width="1.4"/>')
