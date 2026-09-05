"""Shared page furniture: outer card, title, two panels, takeaway bars, footnote."""
import pathlib

from render import render_png
from svgkit import Svg, INK, MUTED, FAINT, PAGE, CARD, EDGE, ARROW, C, tw, shrink

# Diagrams are written straight into the blog post's image directory.
OUT = (pathlib.Path(__file__).resolve().parents[2]
       / "src" / "blog" / "content" / "images" / "learning-llms-2")

W = 1600
PAD = 34            # outer card inset
PANEL_L_X = 70
PANEL_W = 705
PANEL_R_X = 825
GAP = PANEL_R_X - (PANEL_L_X + PANEL_W)   # 50
INNER = 40          # panel inner margin
COL_W = 390         # content column width inside a panel
GUT = 410           # gutter offset from a panel's inner left edge
GUT_W = PANEL_W - 2 * INNER - GUT   # 215


def page(h, title, subtitle):
    s = Svg(W, h)
    s.rect(15, 15, W - 30, h - 30, r=34, fill=PAGE, stroke=EDGE, sw=2.5)
    avail = (PANEL_R_X + PANEL_W) - (PANEL_L_X + 10)
    for txt, size, wt in ((title, 44, 700), (subtitle, 27, 400)):
        if tw(txt, size, wt) > avail:
            print(f"  !! header overflows: {txt!r} {tw(txt, size, wt):.0f} > {avail:.0f}")
    s.text(PANEL_L_X + 10, 100, title, 44, 700, INK)
    s.text(PANEL_L_X + 10, 148, subtitle, 27, 400, MUTED)
    return s


def panel(s, x, top, bottom, section, heading):
    s.rect(x, top, PANEL_W, bottom - top, r=26, fill=CARD, stroke=EDGE, sw=2.5)
    s.text(x + INNER, top + 52, section, 23, 700, MUTED, tracking=1.8)
    s.text(x + INNER, top + 97, heading, 28, 700, INK)
    return x + INNER          # content-column left edge


def takeaway(s, x, y, h, text, kind="out"):
    c = C[kind]
    s.rect(x + INNER, y, PANEL_W - 2 * INNER, h, r=14, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    sz = shrink(text, PANEL_W - 2 * INNER - 30, 25, 700)
    s.text(x + PANEL_W / 2, y + h / 2 + sz * 0.36, text, sz, 700, c["text"], "middle")


def footnote(s, y, text):
    avail = W - 2 * PANEL_L_X
    if tw(text, 22) > avail:
        print(f"  !! footnote overflows: {tw(text, 22):.0f} > {avail:.0f}")
    s.text(W / 2, y, text, 22, 400, FAINT, "middle")


def emit(s, filename):
    """Write the SVG into the blog images directory and rasterize it alongside."""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / filename
    s.save(path)
    render_png(path)
