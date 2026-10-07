"""AUC gain over the raw-score baseline for each model. Redraws Figure 6.

Values were measured off the published figure. The medians match the paper's
text: 2.4%, 21.5% and 27.4% (measured 2.40, 21.55 and 27.39).
"""
from boxplot import Axis, figure, BLUE, GREY

POST = "dependabot-compatibility-score"

ax = Axis(-3, 31, [0, 5, 10, 15, 20, 25, 30], "AUC gain over the baseline's median AUC",
          fmt=lambda t: f"+{t}%" if t else "0%")

figure(POST, "model-auc-gain.svg",
       "The project's own history predicts merges best",
       "Gain in AUC for predicting whether a project merges the PR, across 100 bootstrap runs",
       ax,
       [(None, "Raw score (baseline)", (-1.6, -0.49, 0, 0.31, 1.24), GREY, "median AUC 0.62"),
        (None, "Origin version ranges", (0.42, 1.88, 2.4, 3.03, 4.35), BLUE, "+2.4%"),
        (None, "Client history", (19.04, 20.88, 21.5, 22.17, 24.09), BLUE, "+21.5%"),
        (None, "Both combined", (25.51, 26.7, 27.4, 27.98, 29.66), BLUE, "+27.4%")],
       "Redrawn from Figure 6 of the paper. Box: middle half of runs. Heavy line: median.")
