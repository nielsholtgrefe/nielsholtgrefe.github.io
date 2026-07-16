"""Drawing helpers matching Niels' own figures.

Sources of truth:
  * fig2.svg      — quarnet/pipeline style: black solid tree edges, RED DASHED
                    reticulation arcs with a filled arrowhead into the
                    reticulation, hollow internal nodes, numbered leaves.
  * xiph0/1.svg   — real-data style: strictly ORTHOGONAL cladogram (H/V elbows),
                    leaves right-aligned with italic species labels, red dashed
                    CURVED reticulation arcs (#da0000).
  * scanwidth TikZ — a rooted DAG with CURVED arcs, plus a family of short red
                    "cut" arcs whose colour is graded red!17..red!100; the
                    darkest arc is the maximum, i.e. the scanwidth.
"""

BLACK = "#000000"
RED = "#da0000"          # exactly the xiph reticulation red
GREY = "#8a949b"

EW = 2.0                 # tree edge width
RW = 2.4                 # reticulation edge width
DASH = "7,4.4"           # red dash (ratio as in his figures)


def header(w, h):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="Inter, Helvetica, Arial, sans-serif">'
        f'<defs>'
        f'<marker id="ar" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="5" '
        f'markerHeight="5" orient="auto-start-reverse">'
        f'<path d="M0,1.7 L9,5 L0,8.3 z" fill="{RED}"/></marker>'
        f'<marker id="arb" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="5" '
        f'markerHeight="5" orient="auto-start-reverse">'
        f'<path d="M0,1.7 L9,5 L0,8.3 z" fill="{BLACK}"/></marker>'
        f'</defs>'
    )


def footer():
    return "</svg>"


def edge(p, q, w=EW, color=BLACK):
    return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')


def curve(p, q, bow, w=EW, color=BLACK, dash=None):
    """Quadratic arc from p to q, bowed perpendicular by `bow` (his bend left/right)."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = max((dx * dx + dy * dy) ** 0.5, 1e-6)
    cx, cy = mx - dy / L * bow, my + dx / L * bow
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{p[0]:.1f},{p[1]:.1f} Q{cx:.1f},{cy:.1f} {q[0]:.1f},{q[1]:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{d}/>')


def elbow_hv(p, q, w=EW, color=BLACK):
    """xiph cladogram elbow: vertical from p, then horizontal into q."""
    return (f'<path d="M{p[0]:.1f},{p[1]:.1f} V{q[1]:.1f} H{q[0]:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')


def retic(p, q, bow=0.0, w=RW, arrow=True):
    """Red dashed reticulation arc p -> q with arrowhead at q."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = max((dx * dx + dy * dy) ** 0.5, 1e-6)
    cx, cy = mx - dy / L * bow, my + dx / L * bow
    a = ' marker-end="url(#ar)"' if arrow else ""
    return (f'<path d="M{p[0]:.1f},{p[1]:.1f} Q{cx:.1f},{cy:.1f} {q[0]:.1f},{q[1]:.1f}" '
            f'fill="none" stroke="{RED}" stroke-width="{w}" stroke-dasharray="{DASH}" '
            f'stroke-linecap="round"{a}/>')


def cut_arc(p, q, shade, bow=9.0, w=3.4):
    """A short red 'cut' arc, shaded 0..1 like his red!17..red!100."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = max((dx * dx + dy * dy) ** 0.5, 1e-6)
    cx, cy = mx - dy / L * bow, my + dx / L * bow
    return (f'<path d="M{p[0]:.1f},{p[1]:.1f} Q{cx:.1f},{cy:.1f} {q[0]:.1f},{q[1]:.1f}" '
            f'fill="none" stroke="{RED}" stroke-opacity="{shade:.2f}" '
            f'stroke-width="{w}" stroke-linecap="round"/>')


def arrow(p, q, w=2.4, color=BLACK):
    return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'marker-end="url(#arb)"/>')


def node(p, r=4.4, fill="#ffffff"):
    return (f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{BLACK}" stroke-width="{EW}"/>')


def dot(p, r=4.2, color=BLACK):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{color}"/>'


def rnode(p, r=5.0):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{RED}"/>'


def label(p, s, size=16, anchor="middle", italic=False, color=BLACK, weight="500"):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{p[0]:.1f}" y="{p[1]:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{st}>{s}</text>')


def caption(p, s, size=15):
    return label(p, s, size=size, italic=True, color="#3f4a54", weight="400")


def box(x, y, w, h, r=7, color="#000000", sw=1.0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}" '
            f'fill="none" stroke="{color}" stroke-width="{sw}"/>')
