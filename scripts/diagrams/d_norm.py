from svgkit import Svg, INK, MUTED, FAINT, ARROW, C
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER, COL_W, GUT, GUT_W)

H = 1090
TOP, BOT = 200, 975

s = page(H, "Pre-norm and post-norm: what the residual path passes through",
         "Both blocks normalize. The difference is whether the identity shortcut passes through it.")

MAIN_W, MAIN_OFF = 200, 100      # residual-stream column (offset = centre)
BR_W, BR_OFF = 165, 297          # branch column
HID = (330, 70)
TAP = 442                        # where the branch taps off the residual stream
UPD = (762, 74)
TAKE = (880, 56)
GREEN, AMBER = C["out"]["stroke"], C["pos"]["stroke"]


def stream(x, y0, y1, colour=GREEN, marker=None, sw=6):
    s.path(f"M{x:g} {y0:g} V{y1:g}", stroke=colour, sw=sw, marker=marker)


def add_node(x, y):
    s.plus(x, y, 26, GREEN)
    s.text(x - 40, y + 7, "add", 19, 400, MUTED, "end")


def identity_tag(x, y):
    """A pill sitting on the residual line so the identity path is impossible to miss."""
    w, h = 116, 34
    s.rect(x - w / 2, y - h / 2, w, h, r=17, fill=C["out"]["fill"], stroke=GREEN, sw=2.5)
    s.text(x, y + 7, "identity", 20, 700, C["out"]["text"], "middle")


def block(x, y, h, label, sub=None, kind="qk", w=BR_W):
    s.node(x, y, w, h, label, sub, kind)


def branch_out(mx, bx, y_from, y_to):
    """Residual stream -> branch: tap right, then down into the first branch box."""
    s.path(f"M{mx:g} {y_from:g} H{bx:g} V{y_to:g}", sw=4, marker="aGrey")
    s.circle(mx, y_from, 8, fill=GREEN)


def branch_in(bx, mx, y_from, y_to):
    """Branch output -> back down and left into the add node."""
    s.path(f"M{bx:g} {y_from:g} V{y_to:g} H{mx:g}", sw=4, marker="aGrey")


# ============================================================ LEFT: pre-norm
L = panel(s, PANEL_L_X, TOP, BOT, "PRE-NORM",
          "Normalize the branch, add the result")
LG, LM, LB = PANEL_L_X + INNER + GUT, L + MAIN_OFF, L + BR_OFF
NORM, BLK, ADD = (466, 70), (576, 84), 716

s.node(LM - MAIN_W / 2, HID[0], MAIN_W, HID[1], "hidden", None, "out")
stream(LM, HID[0] + HID[1], ADD - 26)                       # untouched identity path
identity_tag(LM, 545)
branch_out(LM, LB, TAP, NORM[0])
block(LB - BR_W / 2, NORM[0], NORM[1], "norm", None, "pos")
s.path(f"M{LB:g} {NORM[0] + NORM[1]:g} V{BLK[0]:g}", sw=4, marker="aGrey")
block(LB - BR_W / 2, BLK[0], BLK[1], "attention", "or MLP")
branch_in(LB, LM + 26, BLK[0] + BLK[1], ADD)
add_node(LM, ADD)
stream(LM, ADD + 26, UPD[0], marker="aGreen")
s.node(LM - MAIN_W / 2, UPD[0], MAIN_W, UPD[1], "updated hidden", None, "out", label_size=23)

s.wrapped(LG, NORM[0] + 24, "Normalization prepares only the branch input.",
          GUT_W, 22, C["pos"]["text"], 700)
s.wrapped(LG, 636, "The identity path reaches the addition untouched.",
          GUT_W, 22, C["out"]["text"], 700)
takeaway(s, PANEL_L_X, TAKE[0], TAKE[1], "A clean identity path through the block.", "out")

# ============================================================ RIGHT: post-norm
R = panel(s, PANEL_R_X, TOP, BOT, "POST-NORM",
          "Add the result, then normalize the sum")
RG, RM, RB = PANEL_R_X + INNER + GUT, R + MAIN_OFF, R + BR_OFF
BLK2, ADD2, NORM2 = (466, 84), 606, (652, 70)

s.node(RM - MAIN_W / 2, HID[0], MAIN_W, HID[1], "hidden", None, "out")
stream(RM, HID[0] + HID[1], ADD2 - 26)
identity_tag(RM, 490)
branch_out(RM, RB, TAP, BLK2[0])
block(RB - BR_W / 2, BLK2[0], BLK2[1], "attention", "or MLP")
branch_in(RB, RM + 26, BLK2[0] + BLK2[1], ADD2)
add_node(RM, ADD2)
stream(RM, ADD2 + 26, NORM2[0], marker="aGreen")            # the sum is still the residual stream
s.node(RM - MAIN_W / 2, NORM2[0], MAIN_W, NORM2[1], "norm", None, "pos")
stream(RM, NORM2[0] + NORM2[1], UPD[0], colour=AMBER, marker="aAmber", sw=6)
s.node(RM - MAIN_W / 2, UPD[0], MAIN_W, UPD[1], "updated hidden", None, "out", label_size=23)

s.wrapped(RG, BLK2[0] + 24, "The branch reads the hidden state directly.", GUT_W, 22, MUTED)
s.wrapped(RG, NORM2[0] + 22, "The sum is normalized, so the identity path passes through it too.",
          GUT_W, 22, C["pos"]["text"], 700)
takeaway(s, PANEL_R_X, TAKE[0], TAKE[1], "The identity path is normalized.", "pos")

footnote(s, BOT + 46, "At two layers the gap is small. Pre-norm's cleaner gradient route is "
                      "expected to matter more as the stack gets deeper.")
emit(s, "norm-placement-explained.svg")
