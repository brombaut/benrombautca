"""How the posterior narrows as candidate updates accumulate. Appendix figure 1.

Four illustrative success/failure pairs, all scoring 90%, with the candidate count
rising by roughly half an order of magnitude each row. Holding the score fixed
leaves the candidate count as the only thing that varies, so the narrowing is the
only thing the reader has to look at. Computed from the paper's Appendix C, not
traced from its Figure 9, whose own pairs the paper does not state.
"""
from svgkit import INK, MUTED, FAINT
from xyplot import (Scale, BLUE, X0, PX1, posterior, beta_pdf, precision, bounds,
                    polyline, start, x_axis, finish)

POST = "dependabot-compatibility-score"

PAIRS = [(9, 1), (27, 3), (90, 10), (450, 50)]   # every pair scores 90%
SCORE = 0.9

LABEL_W = 300
PX0 = X0 + LABEL_W + 40
ROW_H = 118                    # pitch between rows
CURVE_H = 86                   # drawing height of a row's curve
TOP = 258

xs = Scale(0.4, 1.0, [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
           "true share of candidate updates that would pass, which the score estimates",
           fmt=lambda t: f"{t * 100:.0f}%", p0=PX0, p1=PX1)

axis_y = TOP + len(PAIRS) * ROW_H + 14
h = axis_y + 210
s = start(h, "More candidates, a narrower range of plausible scores",
          "Posterior distribution for four illustrative updates, each scoring 90%",
          axis_y + 120)

x_axis(s, xs, TOP - 8, axis_y)

for i, (succ, fail) in enumerate(PAIRS):
    n = succ + fail
    base = TOP + i * ROW_H + CURVE_H
    a, b = posterior(succ, fail)

    # Each row is scaled to its own peak: the point of the figure is the width of
    # the curve, and the peaks differ by more than 10x from the first row to the last.
    pts = [(x / 1000.0, beta_pdf(x / 1000.0, a, b)) for x in range(400, 1001)]
    peak = max(d for _, d in pts) or 1.0
    polyline(s, [(xs.x(x), base - CURVE_H * d / peak) for x, d in pts], BLUE["stroke"], sw=3)

    lo, hi = bounds(succ, fail)
    s.path(f"M{PX0:g} {base:g} H{PX1:g}", stroke=FAINT, sw=2, cap="butt")
    for e in (lo, hi):
        s.path(f"M{xs.x(e):g} {base + 8:g} V{base - CURVE_H - 6:g}",
               stroke=BLUE["stroke"], sw=2.5, dash="8 7", cap="butt")
    s.path(f"M{xs.x(SCORE):g} {base + 8:g} V{base - CURVE_H - 6:g}",
           stroke=BLUE["text"], sw=4, cap="butt")

    s.text(X0, base - 34, f"{chr(65 + i)}. {succ} of {n} passed", 24, 700, INK)
    s.text(X0, base - 4, f"±{precision(succ, fail) * 100:.1f} points", 22, 400, MUTED)

finish(s, POST, "posterior-narrowing.svg", h,
       "Computed from Appendix C of the paper. Solid line: the compatibility score. "
       "Dashed lines: the bounds of its 90% confidence interval.")
