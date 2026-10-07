"""Candidate updates behind each compatibility score. Redraws Figure 3 of the paper.

Values were measured off the published figure. The 4-tuple median (40.7) matches
the paper's stated median of 41 candidate updates.
"""
from boxplot import Axis, figure, BLUE, AMBER

POST = "dependabot-compatibility-score"
LEGEND = [("3-tuple: every score Dependabot recorded", BLUE),
          ("4-tuple: scores tied to a PR in our projects", AMBER)]

ax = Axis(0.8, 10000, [1, 10, 100, 1000, 10000], "candidate updates behind the score (log scale)",
          log=True, fmt=lambda t: f"{t:,}")

figure(POST, "candidate-updates.svg",
       "Most updates have too few candidates for a badge",
       "Candidate updates behind each compatibility score that has at least one",
       ax,
       [(None, "3-tuple", (1, 1, 1, 3, 15), BLUE, "median 1"),
        (None, "4-tuple", (1, 7, 41, 218, 4730), AMBER, "median 41")],
       "Redrawn from Figure 3 of the paper. Box: middle half of scores. Heavy line: median.",
       legend_items=LEGEND, refs=[(5, "badge shown from 5")])
