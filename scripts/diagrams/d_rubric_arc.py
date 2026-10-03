"""The 12-experiment arc as a ladder: each rubric form labelled by what forced it.

The post walks nine sections in order and the spine is only legible if you read all
of them: three of those sections are diagnostic experiments that produced no new
rubric, they produced the failure that forced the next one. So the layout is a two
column ladder. Left column is what broke, right column is the form adopted in
response, and the right column is chained top to bottom so the arc reads as a
sequence rather than a list of features.

frame.py has no ladder layout (its skeleton is two side-by-side panels), so the
helpers below are local and built on the Svg primitives and frame.py's width
constants only.
"""
from svgkit import Svg, MUTED, FAINT, C, shrink, wrap
from frame import page, footnote, emit, W, PANEL_L_X

POST = "from-checklists-to-prose-verdicts"

# ---------------------------------------------------------------- geometry
X0 = PANEL_L_X                 # 70
X1 = W - PANEL_L_X             # 1530

FAIL_W = 600
FAIL_PAD = 26
FAIL_SZ, FAIL_LH = 24, 32

STAGE_X = 740
STAGE_W = X1 - STAGE_X         # 790
BADGE_DX, BADGE_R = 46, 25
TXT_DX = 98                    # text block offset inside a stage card
STAGE_PAD = 26
TITLE_SZ = 29
DET_SZ, DET_LH = 21, 28

ROW_GAP = 46
TOP = 262                      # first row's top edge
HEAD_Y = 228                   # column headers' baseline

# ---------------------------------------------------------------- content
# (failure that forced it, stage title, what the form became)
ARC = [
    ("A passing test says nothing about design logic",
     "A rubric exists at all",
     "Two skills, primitive structure, rubric logic left in the prompt"),
    ("A rubric that mixes clean with correct measures neither",
     "Architecture split from correctness",
     "Correctness out of scope, weighted 0-1 items per axis"),
    ("The checklist rewarded local compliance and missed parallel mechanisms",
     "Holistic 0-5 axis scoring",
     "Discrete levels read as descriptions, one judgment per axis"),
    ("At 9 issues: drifting baselines, no removal check, uneven exploration",
     "Committed methodology",
     "Baselines committed, removals checked, depth held uniform"),
    ("The audit found the prompts overfit to Django and Astropy",
     "Codebase-derived axes",
     "Exploration picks the axes, boundary calls documented"),
    ("Numeric scores implied precision the process could not support",
     "Prose verdicts",
     "Prose per-axis assessments, verdicts of High, Acceptable, Low"),
]

FAIL_AVAIL = FAIL_W - 2 * FAIL_PAD
DET_AVAIL = STAGE_W - TXT_DX - STAGE_PAD

# Measure every string before any box is sized, then stack the rows.
rows = []
y = TOP
for i, (fail, title, detail) in enumerate(ARC):
    fl = wrap(fail, FAIL_AVAIL, FAIL_SZ, 700)
    dl = wrap(detail, DET_AVAIL, DET_SZ)
    fail_h = 2 * FAIL_PAD + len(fl) * FAIL_LH
    stage_h = 2 * STAGE_PAD + TITLE_SZ + 14 + len(dl) * DET_LH
    h = max(fail_h, stage_h, 2 * BADGE_R + 44)
    rows.append(dict(y=y, h=h, fail=fl, title=title, detail=dl,
                     kind="out" if i == len(ARC) - 1 else "token"))
    y += h + ROW_GAP

LAST = rows[-1]
FOOT_Y = LAST["y"] + LAST["h"] + 92
H = FOOT_Y + 52

s = page(H, "Twelve experiments, six rubric forms",
         "Every form was adopted because the previous one failed under comparison.")

s.text(X0, HEAD_Y, "WHAT BROKE", 23, 700, MUTED, tracking=1.8)
s.text(STAGE_X, HEAD_Y, "WHAT THE RUBRIC BECAME", 23, 700, MUTED, tracking=1.8)


def failure_card(r):
    """Amber card: the failure, in its own words, sized to the wrapped lines."""
    c = C["pos"]
    s.rect(X0, r["y"], FAIL_W, r["h"], r=18, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    block = len(r["fail"]) * FAIL_LH
    base = r["y"] + (r["h"] - block) / 2 + FAIL_SZ * 0.82
    for i, ln in enumerate(r["fail"]):
        s.text(X0 + FAIL_PAD, base + i * FAIL_LH, ln, FAIL_SZ, 700, c["text"])


def stage_card(r, n):
    c = C[r["kind"]]
    s.rect(STAGE_X, r["y"], STAGE_W, r["h"], r=18, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    cy = r["y"] + r["h"] / 2
    s.circle(STAGE_X + BADGE_DX, cy, BADGE_R, fill="#ffffff", stroke=c["stroke"], sw=2.5)
    s.text(STAGE_X + BADGE_DX, cy + BADGE_R * 0.36, str(n), 25, 700, c["text"], "middle")
    tx = STAGE_X + TXT_DX
    block = TITLE_SZ + 14 + len(r["detail"]) * DET_LH
    top = r["y"] + (r["h"] - block) / 2
    sz = shrink(r["title"], DET_AVAIL, TITLE_SZ, 700)
    s.text(tx, top + sz * 0.82, r["title"], sz, 700, c["text"])
    for i, ln in enumerate(r["detail"]):
        s.text(tx, top + TITLE_SZ + 14 + (i + 1) * DET_LH - 7, ln, DET_SZ, 400, MUTED)


for n, r in enumerate(rows, 1):
    failure_card(r)
    stage_card(r, n)
    cy = r["y"] + r["h"] / 2
    s.path(f"M{X0 + FAIL_W:g} {cy:g} H{STAGE_X:g}", stroke=C["pos"]["stroke"], sw=3.5,
           marker="aAmber")

# The spine: the right column is one chain, which is what makes it an arc.
for a, b in zip(rows, rows[1:]):
    x = STAGE_X + BADGE_DX
    s.path(f"M{x:g} {a['y'] + a['h']:g} V{b['y']:g}", sw=3.5, marker="aGrey")

s.text(STAGE_X, LAST["y"] + LAST["h"] + 44, "Prose is where it stands now, not where it ends.",
       22, 400, FAINT)

footnote(s, FOOT_Y, "Three experiments produced no new rubric: the first 6-issue run, the "
                    "scale-up to 9, and the consistency audit. They produced the failures.")
emit(s, POST, "twelve-experiment-arc.svg")
