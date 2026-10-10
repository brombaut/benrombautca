"""How fast the interval tightens as candidate updates accumulate. Appendix figure 2.

Interval precision against candidate count, for three observed scores. The two
reference lines are the medians the post already quotes from Figure 8: 15 points
for the 3-tuple scores and 3.5 for the 4-tuple ones. Computed from the paper's
Appendix C.
"""
from svgkit import INK, MUTED, FAINT, EDGE
from xyplot import (Scale, BLUE, AMBER, TEAL, X0, PX1, precision, polyline,
                    start, x_axis, legend, finish)

POST = "dependabot-compatibility-score"

SERIES = [(1.00, "a score of 100%", BLUE),
          (0.95, "95%", AMBER),
          (0.90, "90%", TEAL)]

PX0 = X0 + 110
TOP = 320
PLOT_H = 470

xs = Scale(5, 5000, [5, 10, 50, 100, 500, 1000, 5000], "candidate updates behind the score",
           log=True, fmt=lambda t: f"{t:,}", p0=PX0, p1=PX1)
ys = Scale(0, 30, [0, 5, 10, 15, 20, 25, 30], "", p0=TOP + PLOT_H, p1=TOP)

axis_y = TOP + PLOT_H
h = axis_y + 250
s = start(h, "Reaching a narrow interval takes hundreds of candidates",
          "Width of the 90% confidence interval, by candidate count and observed score",
          axis_y + 160)

s.text(PX0, TOP - 26, "percentage points from the score to its furthest bound",
       22, 400, MUTED)
x_axis(s, xs, TOP, axis_y)
for t in ys.ticks:
    gy = ys.y(t)
    s.path(f"M{PX0:g} {gy:g} H{PX1:g}", stroke=EDGE, sw=2, dash="5 8", cap="butt")
    s.text(PX0 - 18, gy + 8, f"{t}", 21, 400, FAINT, "end")

# The two medians the post quotes, so the curve reads against numbers already given.
for v, label in ((15, "3-tuple median, 15 points"), (3.5, "4-tuple median, 3.5 points")):
    gy = ys.y(v)
    s.path(f"M{PX0:g} {gy:g} H{PX1:g}", stroke=MUTED, sw=2.5, dash="9 7", cap="butt")
    s.text(PX1 - 6, gy - 14, label, 20, 700, MUTED, "end")

for score, label, c in SERIES:
    # Successes are left real rather than rounded to whole PRs: at small n the
    # rounding puts a visible sawtooth on the curve, and the question here is how
    # the width scales with n, not which counts are reachable at a given n.
    pts = []
    n = 5.0
    while n <= 5000:
        pts.append((xs.x(n), ys.y(precision(score * n, (1 - score) * n) * 100)))
        n *= 1.04
    pts.append((xs.x(5000), ys.y(precision(score * 5000, (1 - score) * 5000) * 100)))
    polyline(s, pts, c["stroke"], sw=4)

legend(s, axis_y + 132, PX0, [(l if "score" in l else f"a score of {l}", c)
                              for _, l, c in SERIES])

finish(s, POST, "precision-vs-candidates.svg", h,
       "Computed from Appendix C of the paper. The badge appears at 5 candidate updates, "
       "where the leftmost point of each curve sits.")
