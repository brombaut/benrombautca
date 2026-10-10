"""Continuous-curve plots on the house frame, for the confidence-interval appendix.

`boxplot.py` draws five-number summaries measured off a published figure. These
plots are different: the curves here are *computed* from the paper's formulas
(Appendix C), so the numbers are exact rather than traced, and the generators say
which pairs they illustrate.

The shared pieces are the card, the x axis, the legend and the two statistics the
appendix turns on: the posterior density and the interval precision.
"""
import math

from svgkit import Svg, INK, MUTED, FAINT, EDGE, CARD, C, tw, WARN
from frame import page, footnote, emit, W, PANEL_L_X

BLUE = C["token"]
AMBER = dict(stroke="#c2741a", fill="#fcefdc", text="#8a4f0c")
TEAL = C["v"]

X0 = PANEL_L_X                 # left edge of the card's content
PX1 = W - PANEL_L_X - 20


class Scale:
    """Maps a data value onto a pixel range, linearly or on a log axis."""

    def __init__(self, lo, hi, ticks, title, log=False, fmt=str, p0=0, p1=0):
        self.lo, self.hi, self.ticks, self.title = lo, hi, ticks, title
        self.log, self.fmt, self.p0, self.p1 = log, fmt, p0, p1

    def frac(self, v):
        if self.log:
            return ((math.log10(v) - math.log10(self.lo))
                    / (math.log10(self.hi) - math.log10(self.lo)))
        return (v - self.lo) / (self.hi - self.lo)

    def x(self, v):
        return self.p0 + (self.p1 - self.p0) * self.frac(v)

    def y(self, v):
        return self.p0 + (self.p1 - self.p0) * self.frac(v)


# ------------------------------------------------------------ the paper's maths
def posterior(successes, failures):
    """The Beta posterior from a uniform Beta(1, 1) prior. Appendix C."""
    return 1 + successes, 1 + failures


def beta_pdf(x, a, b):
    """Density of Beta(a, b), in log space so large a and b don't overflow."""
    if x <= 0 or x >= 1:
        return 0.0
    lg = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
          + (a - 1) * math.log(x) + (b - 1) * math.log1p(-x))
    return math.exp(lg)


def precision(successes, failures):
    """1.65 standard deviations of the posterior, the paper's Precision_CI."""
    a, b = posterior(successes, failures)
    sd = math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
    return 1.65 * sd


def bounds(successes, failures):
    """The 90% interval, clamped to [0, 1] as the paper defines it."""
    score = successes / (successes + failures)
    p = precision(successes, failures)
    return max(score - p, 0.0), min(score + p, 1.0)


# ------------------------------------------------------------------ furniture
def legend(s, y, x, items):
    """One row of swatch + label pairs, starting at `x`."""
    for label, c in items:
        s.rect(x, y - 19, 34, 24, r=6, fill=c["fill"], stroke=c["stroke"], sw=2.5)
        s.text(x + 46, y, label, 22, 400, MUTED)
        x += 46 + tw(label, 22) + 44
    if x - 44 > PX1:
        WARN.append(f"legend runs past the plot: {x - 44:.0f} > {PX1}")


def polyline(s, pts, stroke, sw=3.5, dash=None):
    d = "M" + " L".join(f"{x:g} {y:g}" for x, y in pts)
    s.path(d, stroke=stroke, sw=sw, dash=dash)


def start(h, title, subtitle, card_bottom):
    s = page(h, title, subtitle)
    s.rect(PANEL_L_X - 30, 180, W - 2 * PANEL_L_X + 60, card_bottom - 180, r=26,
           fill=CARD, stroke=EDGE, sw=2.5)
    return s


def x_axis(s, xs, top, axis_y, label_gap=34):
    """Dashed gridlines, tick labels and the axis title."""
    for t in xs.ticks:
        gx = xs.x(t)
        s.path(f"M{gx:g} {top:g} V{axis_y:g}", stroke=EDGE, sw=2, dash="5 8", cap="butt")
        s.text(gx, axis_y + label_gap, xs.fmt(t), 21, 400, FAINT, "middle")
    s.path(f"M{xs.p0:g} {axis_y:g} H{xs.p1:g}", stroke=EDGE, sw=2.5, cap="butt")
    s.text((xs.p0 + xs.p1) / 2, axis_y + label_gap + 42, xs.title, 23, 400, MUTED, "middle")


def finish(s, post, filename, h, foot):
    footnote(s, h - 48, foot)
    emit(s, post, filename)
