from svgkit import MUTED, C, shrink
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER)

POST = "learning-to-use-ai-coding-tools"

H = 1100
TOP, BOT = 200, 1000

# One skeleton, used by both panels: three stage rows in a "in the loop" column,
# one "on the side" column, a unit-of-review band, a takeaway bar.
HDR_Y = 352                       # column headers
ROWS = (376, 506, 636)            # stage row tops
ROW_H = 80
MAIN_X, MAIN_W = 110, 190         # offsets from a panel's content-column left edge
SIDE_X, SIDE_W = 415, 210
BAND_X, BAND_W = 110, 515
UNIT_LBL_Y, BAND_Y, BAND_H = 776, 792, 76
TAKE_Y, TAKE_H = 906, 56
STAGES = ("intent", "code", "review")
GHOST_DASH = "7 7"


def row_mid(i):
    return ROWS[i] + ROW_H / 2


def skeleton(x, occupants, side):
    """Draw one panel's grid. `occupants` is three (label, sub, kind) triples."""
    s.text(x + MAIN_X + MAIN_W / 2, HDR_Y, "IN THE LOOP", 19, 700, MUTED, "middle", tracking=1.6)
    s.text(x + SIDE_X + SIDE_W / 2, HDR_Y, "ON THE SIDE", 19, 700, MUTED, "middle", tracking=1.6)

    for i, (stage, (label, sub, kind)) in enumerate(zip(STAGES, occupants)):
        s.text(x + MAIN_X - 22, row_mid(i) + 8, stage, 23, 700, MUTED, "end")
        s.node(x + MAIN_X, ROWS[i], MAIN_W, ROW_H, label, sub, kind)
        if i:   # flow arrow from the previous stage into this one
            s.path(f"M{x + MAIN_X + MAIN_W / 2:g} {ROWS[i - 1] + ROW_H:g} V{ROWS[i]:g}",
                   sw=4, marker="aGrey")

    s.node(x + SIDE_X, ROWS[1], SIDE_W, ROW_H, side[0], side[1], "ghost", dash=GHOST_DASH)


def band(x, text):
    c = C["pos"]
    s.text(x + BAND_X, UNIT_LBL_Y, "UNIT OF REVIEW", 19, 700, MUTED, tracking=1.6)
    s.rect(x + BAND_X, BAND_Y, BAND_W, BAND_H, r=16, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    sz = shrink(text, BAND_W - 40, 25, 700, floor=20)
    s.text(x + BAND_X + BAND_W / 2, BAND_Y + BAND_H / 2 + sz * 0.36, text, sz, 700,
           c["text"], "middle")


s = page(H, "Where I sit in the loop: early 2023, and the end of 2025",
         "The same three stages both times. What moves is who holds the middle one, "
         "and what I actually review.")

# ============================================================ LEFT: early 2023
L = panel(s, PANEL_L_X, TOP, BOT, "EARLY 2023",
          "I write the code, the agent is consulted")
skeleton(L, (("me", "what I want", "token"),
             ("me", "I write it", "token"),
             ("me", "I read the output", "token")),
         ("ChatGPT", "in a browser tab"))

# The only contact with the agent: paste something over, paste something back.
gap_l, gap_r = L + MAIN_X + MAIN_W, L + SIDE_X
mid = row_mid(1)
s.path(f"M{gap_l + 6:g} {mid - 13:g} H{gap_r - 4:g}", stroke=C["ghost"]["stroke"], sw=3,
       marker="aFaint", dash="6 6")
s.path(f"M{gap_r - 4:g} {mid + 13:g} H{gap_l + 6:g}", stroke=C["ghost"]["stroke"], sw=3,
       marker="aFaint", dash="6 6")
s.text((gap_l + gap_r) / 2, mid + 38, "copy-paste", 18, 400, MUTED, "middle")

band(L, "a pasted function, read line by line")
takeaway(s, PANEL_L_X, TAKE_Y, TAKE_H, "\"Google was still my default\"", "token")

# ============================================================ RIGHT: end of 2025
R = panel(s, PANEL_R_X, TOP, BOT, "END OF 2025",
          "The agent writes the code, I describe and review")
skeleton(R, (("me", "what I want", "token"),
             ("agent", "it writes it", "qk"),
             ("me", "I read the output", "token")),
         ("chat tools", "open, off the path"))

band(R, "a described outcome, judged as a whole")
takeaway(s, PANEL_R_X, TAKE_Y, TAKE_H,
         "\"barely resembles what I'd have called coding\"", "out")

footnote(s, BOT + 46, "Activation energy is what changed most: starting used to mean holding the "
                      "codebase in my head, now it means starting a conversation.")
emit(s, POST, "human-in-the-loop.svg")
