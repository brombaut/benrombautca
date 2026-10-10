"""Width of each score's 90% confidence interval. Redraws Figure 8.

Values were measured off the published figure. The medians match the paper's
text: over 15% for half the 3-tuple scores (measured 14.9) and 3.5% for the
4-tuple scores (measured 3.46).
"""
from boxplot import Axis, figure, BLUE, AMBER

POST = "dependabot-compatibility-score"
LEGEND = [("3-tuple: every score Dependabot recorded", BLUE),
          ("4-tuple: scores tied to a PR in our projects", AMBER)]

ax = Axis(0, 35, [0, 5, 10, 15, 20, 25, 30, 35], "percentage points from the score to its furthest 90% bound",
          fmt=lambda t: f"{t}")

figure(POST, "confidence-interval-width.svg",
       "Many shown scores come with a wide confidence interval",
       "Scores with at least 5 candidate updates",
       ax,
       [(None, "3-tuple", (0.3, 8.88, 14.92, 20.39, 28.89), BLUE, "median 15"),
        (None, "4-tuple", (0.34, 1.36, 3.46, 9.12, 20.56), AMBER, "median 3.5")],
       "Redrawn from Figure 8 of the paper. Box: middle half of scores. Heavy line: median.",
       legend_items=LEGEND)
