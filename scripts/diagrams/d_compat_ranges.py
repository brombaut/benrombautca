"""Candidates gained by widening the origin version range. Redraws Figure 5.

Values were measured off the published figure. The medians match the paper's
text: 1x, 5x and 10x for the 3-tuple dataset, and 1x, 1.5x and 1.9x for the
4-tuple dataset (measured 1.0, 1.50 and 1.84).
"""
from boxplot import Axis, figure, BLUE, AMBER

POST = "dependabot-compatibility-score"
LEGEND = [("3-tuple: every score Dependabot recorded", BLUE),
          ("4-tuple: scores tied to a PR in our projects", AMBER)]

ax = Axis(0.8, 3000, [1, 10, 100, 1000], "candidates as a multiple of the exact-version score (log scale)",
          log=True, fmt=lambda t: f"{t:,}x")

figure(POST, "origin-version-ranges.svg",
       "Wider origin version ranges draw on more candidates",
       "Candidate updates behind each range score, relative to the exact-version score",
       ax,
       [("PATCH RANGE  x.y.*", "3-tuple", (1, 1, 1, 3, 15.5), BLUE, "median 1x"),
        ("PATCH RANGE  x.y.*", "4-tuple", (1, 1, 1, 1.38, 2.24), AMBER, "median 1x"),
        ("MINOR RANGE  x.*.*", "3-tuple", (1, 1.49, 5, 21, 1090), BLUE, "median 5x"),
        ("MINOR RANGE  x.*.*", "4-tuple", (1, 1.12, 1.5, 2.94, 12.6), AMBER, "median 1.5x"),
        ("MAJOR RANGE  *.*.*", "3-tuple", (1, 2.29, 10, 35.1, 2080), BLUE, "median 10x"),
        ("MAJOR RANGE  *.*.*", "4-tuple", (1, 1.29, 1.84, 4.26, 25.6), AMBER, "median 1.9x")],
       "Redrawn from Figure 5 of the paper. Box: middle half of scores. Heavy line: median.",
       legend_items=LEGEND)
