"""Horizontal box plots on the house frame, for figures redrawn from a published paper.

Nothing here reads raw data. Each row is given as the five numbers a box plot is
drawn from (whisker ends, quartiles, median), measured off the published figure, so
the result is a faithful redraw of what the paper shows rather than a recomputation.
The generators that use this say which figure they redraw and where the values
were checked against numbers stated in the paper's text.

Colour: two series need two colours, blue (`token`) and an amber darker than
frame.C's `pos`. That amber stroke clears 3:1 against the white card, which `pos`
(#d08a1e) does not, and the pair passes the dataviz palette validator for
colour-blind separation. Colour never carries identity alone: every row is named.
"""
import math

from svgkit import Svg, INK, MUTED, FAINT, EDGE, CARD, C, tw, shrink, WARN
from frame import page, footnote, emit, W, PANEL_L_X

BLUE = C["token"]
AMBER = dict(stroke="#c2741a", fill="#fcefdc", text="#8a4f0c")
GREY = C["ghost"]

X0 = PANEL_L_X                 # left edge of the card's content
LABEL_W = 330                  # row-label column
PX0 = X0 + LABEL_W + 40        # plot area
PX1 = W - PANEL_L_X - 20
PW = PX1 - PX0

ROW = 92                       # pitch between rows
BOX_H = 38
GROUP_GAP = 34                 # extra space above each group heading


class Axis:
    def __init__(self, lo, hi, ticks, title, log=False, fmt=str):
        self.lo, self.hi, self.ticks, self.title, self.log, self.fmt = lo, hi, ticks, title, log, fmt

    def x(self, v):
        if self.log:
            f = (math.log10(v) - math.log10(self.lo)) / (math.log10(self.hi) - math.log10(self.lo))
        else:
            f = (v - self.lo) / (self.hi - self.lo)
        return PX0 + PW * f


def legend(s, y, items):
    """One row of swatch + label pairs, left-aligned with the plot area."""
    x = PX0
    for label, c in items:
        s.rect(x, y - 19, 34, 24, r=6, fill=c["fill"], stroke=c["stroke"], sw=2.5)
        s.text(x + 46, y, label, 22, 400, MUTED)
        x += 46 + tw(label, 22) + 44
    if x - 44 > PX1:
        WARN.append(f"legend runs past the plot: {x - 44:.0f} > {PX1}")


def box(s, ax, y, stats, c, note=None):
    """One box: whiskers with caps, a quartile box, a heavy median, an optional note."""
    lo, q1, med, q3, hi = (ax.x(v) for v in stats)
    cy = y + BOX_H / 2
    for a, b in ((lo, q1), (q3, hi)):
        if b - a > 1:
            s.path(f"M{a:g} {cy:g} H{b:g}", stroke=c["stroke"], sw=3, cap="butt")
    for e in (lo, hi):
        s.path(f"M{e:g} {cy - 11:g} V{cy + 11:g}", stroke=c["stroke"], sw=3, cap="round")
    s.rect(q1, y, max(q3 - q1, 3), BOX_H, r=7, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    s.path(f"M{med:g} {y - 5:g} V{y + BOX_H + 5:g}", stroke=c["text"], sw=5, cap="round")
    if note:
        # The median note sits above its box, flipped to end there if it would
        # run off the right edge of the plot.
        nw = tw(note, 20, 700)
        if med + nw / 2 > PX1:
            s.text(med, y - 12, note, 20, 700, c["text"], "end")
        elif med - nw / 2 < PX0:
            s.text(med, y - 12, note, 20, 700, c["text"], "start")
        else:
            s.text(med, y - 12, note, 20, 700, c["text"], "middle")


def figure(post, filename, title, subtitle, ax, rows, foot, legend_items=None,
           refs=(), top_pad=0):
    """Rows are (group_heading or None, label, stats, colour, median_note)."""
    # Lay rows out first so the page height follows the content.
    y = 214 + (76 if legend_items else 40) + top_pad
    plot_top = y - 30
    placed, last_group = [], None
    for group, label, stats, c, note in rows:
        if group and group != last_group:
            if placed:
                y += GROUP_GAP
            placed.append(("group", group, y))
            y += 46
            last_group = group
        placed.append(("row", (label, stats, c, note), y))
        y += ROW
    plot_bot = y - ROW + BOX_H + 30
    axis_y = plot_bot
    h = axis_y + 200

    s = page(h, title, subtitle)
    s.rect(PANEL_L_X - 30, 180, W - 2 * PANEL_L_X + 60, axis_y + 110 - 180, r=26,
           fill=CARD, stroke=EDGE, sw=2.5)
    if legend_items:
        legend(s, 236, legend_items)

    # Gridlines and ticks first, so marks sit on top of them.
    for t in ax.ticks:
        gx = ax.x(t)
        s.path(f"M{gx:g} {plot_top:g} V{axis_y:g}", stroke=EDGE, sw=2, dash="5 8", cap="butt")
        s.text(gx, axis_y + 34, ax.fmt(t), 21, 400, FAINT, "middle")
    s.path(f"M{PX0:g} {axis_y:g} H{PX1:g}", stroke=EDGE, sw=2.5, cap="butt")
    s.text((PX0 + PX1) / 2, axis_y + 76, ax.title, 23, 400, MUTED, "middle")

    for v, label in refs:
        rx = ax.x(v)
        s.path(f"M{rx:g} {plot_top - 4:g} V{axis_y:g}", stroke=MUTED, sw=2.5, dash="9 7", cap="butt")
        s.text(rx + 10, plot_top + 12, label, 19, 700, MUTED)

    for kind, item, ry in placed:
        if kind == "group":
            s.text(X0, ry + 4, item, 20, 700, FAINT, tracking=1.8)
            continue
        label, stats, c, note = item
        sz = shrink(label, LABEL_W, 23, 700)
        s.text(X0, ry + BOX_H / 2 + 8, label, sz, 700, INK)
        box(s, ax, ry, stats, c, note)

    footnote(s, h - 48, foot)
    emit(s, post, filename)
