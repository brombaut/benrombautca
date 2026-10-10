"""Compatibility scores that clear the 5-candidate threshold. Redraws Figure 4.

Values were measured off the published figure. For the 3-tuple dataset the upper
quartile, median and upper whisker all sit at 100%.
"""
from boxplot import Axis, figure, BLUE, AMBER

POST = "dependabot-compatibility-score"
LEGEND = [("3-tuple: every score Dependabot recorded", BLUE),
          ("4-tuple: scores tied to a PR in our projects", AMBER)]

ax = Axis(0, 100, [0, 20, 40, 60, 80, 100], "compatibility score", fmt=lambda t: f"{t}%")

figure(POST, "shown-scores.svg",
       "The scores that do get shown sit near 100%",
       "Compatibility scores with at least 5 candidate updates",
       ax,
       [(None, "3-tuple", (75, 90, 100, 100, 100), BLUE, "median 100%"),
        (None, "4-tuple", (88, 95, 98, 100, 100), AMBER, "median 98%")],
       "Redrawn from Figure 4 of the paper. Box: middle half of scores. Heavy line: median.",
       legend_items=LEGEND)
