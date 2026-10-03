"""The eleven slop families, laid out against the three tooling modes.

The post's "Common Thread" section is the only place the families are grouped by
anything other than their numbering, and several families appear in more than one
mode because the mode depends on the rule rather than the family. So the layout is
a row per family and a column per mode, where one family's card spans every column
it belongs to. A card wider than one column is a family that straddles.

No such grid exists in frame.py; the helpers below are local on purpose.
"""
from frame import page, footnote, emit
from svgkit import INK, MUTED, FAINT, EDGE, CARD, C, shrink, wrap

POST = "ai-slop-eleven-families"

# ---------------------------------------------------------------- geometry
LBL_X = 70
LBL_W = 505
BX = [600, 918, 1236]      # mode-column left edges
BW = 304
RIGHT = BX[2] + BW         # 1540

HDR_TOP = 196
HDR_H = 128
GRID_TOP = HDR_TOP + HDR_H + 22
PITCH = 66
CARD_H = 54
CHIP_H = 38

MODES = [
    ("out",   "Deterministic", "A linter, an AST pass or a CI gate can clear it"),
    ("pos",   "Needs judgment", "A tool proposes candidates, a person decides"),
    ("qk",    "Workflow control", "Cheaper to prevent than to detect afterwards"),
]

# family: (number, name, damage gloss, {mode index: chip label})
FAMILIES = [
    (1,  "Hygiene Debris", "dead weight left in the tree",
     {0: "static, no LLM needed"}),
    (2,  "Annotation Noise", "noise in the comment layer",
     {0: "many rules, not all"}),
    (3,  "Redundant Guarding", "obscures the real invariants",
     {1: "needs type context"}),
    (4,  "Structural Bloat", "indirection without payoff",
     {1: "is the abstraction earned?", 2: "architecture reinvention"}),
    (5,  "Duplication by Regeneration", "many copies of one idea",
     {1: "semantic clones", 2: "search before write"}),
    (6,  "Test Slop", "tests that cannot fail",
     {1: "circular, zero-assertion", 2: "test weakening"}),
    (7,  "Integrity and Fake-Done", "false claims of done",
     {0: "shallow stubs, leakage", 1: "deep violations", 2: "verification gaming"}),
    (8,  "Error-Swallowing", "errors that never surface",
     {0: "empty catch, bare except", 1: "semantic swallowing"}),
    (9,  "Type Laxity", "type guarantees voided",
     {0: "as any, double cast"}),
    (10, "Kinetic Slop", "diffs wider than the request",
     {2: "scope held at the harness"}),
    (11, "Naming Drift", "names that carry no meaning",
     {}),
]


def band_backgrounds(s, top, bottom):
    for i in range(3):
        s.rect(BX[i], top, BW, bottom - top, r=18,
               fill="#f7f9fd", stroke=EDGE, sw=2)


def mode_header(s, i):
    kind, title, desc = MODES[i]
    c = C[kind]
    s.rect(BX[i], HDR_TOP, BW, HDR_H, r=18, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    sz = shrink(title, BW - 30, 27, 700)
    s.text(BX[i] + BW / 2, HDR_TOP + 44, title, sz, 700, c["text"], "middle")
    lines = wrap(desc, BW - 34, 19, 400)
    for j, ln in enumerate(lines):
        s.text(BX[i] + BW / 2, HDR_TOP + 76 + j * 25, ln, 19, 400, MUTED, "middle")


def family_row(s, idx, num, name, gloss, chips):
    y = GRID_TOP + idx * PITCH
    cy = y + CARD_H / 2

    # left label column: numbered badge, family name, the damage it does
    s.circle(LBL_X + 22, cy, 20, fill=CARD, stroke=EDGE, sw=2.5)
    s.text(LBL_X + 22, cy + 8, str(num), 22, 700, MUTED, "middle")
    tx = LBL_X + 56
    avail = LBL_W - 56
    s.text(tx, cy - 7, name, shrink(name, avail, 25, 700), 700, INK)
    s.text(tx, cy + 18, gloss, shrink(gloss, avail, 20, 400), 400, MUTED)

    if not chips:
        s.rect(BX[0], y, RIGHT - BX[0], CARD_H, r=14, fill="none",
               stroke=FAINT, sw=2.5, dash="9 8")
        msg = "the post's three lists do not place it"
        s.text((BX[0] + RIGHT) / 2, cy + 7, msg,
               shrink(msg, RIGHT - BX[0] - 40, 20, 400), 400, FAINT, "middle")
        return

    cols = sorted(chips)
    lo, hi = cols[0], cols[-1]
    # A family that belongs to more than one mode gets one slab crossing the
    # column gaps, so straddling is visible as width rather than as repetition.
    if hi > lo:
        s.rect(BX[lo] + 4, y, BX[hi] + BW - BX[lo] - 8, CARD_H, r=15,
               fill="#e6ecf5", stroke="#9aabc3", sw=2.5)
        # a solid bridge across each column gap: the straddle, made unmissable
        for i in range(lo, hi):
            x0 = BX[i] + BW - 16
            x1 = BX[i + 1] + 16
            s.rect(x0, cy - 9, x1 - x0, 18, r=5, fill="#9aabc3")
    for i in cols:
        c = C[MODES[i][0]]
        s.rect(BX[i] + 12, cy - CHIP_H / 2, BW - 24, CHIP_H, r=11,
               fill=c["fill"], stroke=c["stroke"], sw=2)
        lbl = chips[i]
        s.text(BX[i] + BW / 2, cy + 7, lbl,
               shrink(lbl, BW - 44, 20, 600), 600, c["text"], "middle")


def takeaway_bar(s, y, h, text, kind="pos"):
    c = C[kind]
    s.rect(LBL_X, y, RIGHT - LBL_X, h, r=16, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    sz = shrink(text, RIGHT - LBL_X - 44, 26, 700)
    s.text((LBL_X + RIGHT) / 2, y + h / 2 + sz * 0.36, text, sz, 700, c["text"], "middle")


def build():
    grid_bottom = GRID_TOP + len(FAMILIES) * PITCH - (PITCH - CARD_H) + 14
    take_y = grid_bottom + 30
    take_h = 66
    h = take_y + take_h + 74

    s = page(h, "Eleven slop families, three ways to fix them",
             "The grouping from the conclusion, and the families that straddle it")

    s.text(LBL_X, HDR_TOP + 54, "FAMILY", 21, 700, FAINT, tracking=2.0)
    s.text(LBL_X, HDR_TOP + 86, "and the damage it does", 19, 400, FAINT)

    band_backgrounds(s, GRID_TOP - 14, grid_bottom)
    for i in range(3):
        mode_header(s, i)
    for idx, (num, name, gloss, chips) in enumerate(FAMILIES):
        family_row(s, idx, num, name, gloss, chips)

    takeaway_bar(s, take_y, take_h,
                 "Five of the eleven sit in more than one column: the mode is a property of the rule")
    footnote(s, h - 36,
             "Sub-patterns from the post's lists are folded into their parent family; "
             "cross-language leakage sits under Integrity.")
    emit(s, POST, "slop-families-tooling-modes.svg")


if __name__ == "__main__":
    build()
