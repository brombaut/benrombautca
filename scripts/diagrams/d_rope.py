from svgkit import Svg, INK, MUTED, FAINT, ARROW, C
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER, COL_W, GUT, GUT_W)

H = 1030
TOP, BOT = 200, 940

s = page(H, "Where position enters the model",
         "Absolute embeddings change the token vector. RoPE changes how two tokens compare.")

R1 = (330, 78)      # input row                      (y, h)
R2 = (452, 84)      # the vector that enters attention
R3 = (596, 80)      # Q / K / V chips
R4 = (726, 86)      # outcome
TAKE = (852, 58)

BOX_W = 168                                   # row-1 boxes
QK_W, V_W = 108, 130                          # chip widths
CHIP = [(0, QK_W), (130, QK_W), (260, V_W)]   # (offset, width) inside the content column


def arrow_down(x, y0, y1, colour=ARROW, marker="aGrey", dash=None):
    s.path(f"M{x:g} {y0:g} V{y1:g}", stroke=colour, sw=3.5, marker=marker, dash=dash)


def fan(x_from, y0, y1, targets):
    """One trunk down to a bus line, then a short tick into each chip."""
    mid = (y0 + y1) / 2
    s.path(f"M{x_from:g} {y0:g} V{mid:g}", sw=3.5)
    s.path(f"M{min(targets):g} {mid:g} H{max(targets):g}", sw=3.5)
    for t in targets:
        s.path(f"M{t:g} {mid:g} V{y1:g}", sw=3.5, marker="aGrey")


def input_row(x, ghost):
    """token (+) position. On the RoPE side the addition is drawn as the thing that never happens."""
    y, h = R1
    s.node(x, y, BOX_W, h, "token", "“cat”", "token")
    s.plus(x + COL_W / 2, y + h / 2, color="#c3ccdb" if ghost else ARROW,
           opacity=0.75 if ghost else None)
    s.node(x + COL_W - BOX_W, y, BOX_W, h, "position 3",
           "never added" if ghost else "learned vector", "ghost" if ghost else "pos",
           dash="8 7" if ghost else None)
    for x0, x1 in [(x + BOX_W, x + COL_W / 2 - 32), (x + COL_W - BOX_W, x + COL_W / 2 + 32)]:
        if ghost:
            s.path(f"M{x0:g} {y + h / 2:g} H{x1:g}", stroke="#c3ccdb", sw=3.5,
                   marker="aFaint", dash="8 7")
        else:
            s.path(f"M{x0:g} {y + h / 2:g} H{x1:g}", sw=3.5, marker="aGrey")


# ============================================================ LEFT: absolute
L = panel(s, PANEL_L_X, TOP, BOT, "LEARNED ABSOLUTE POSITIONS",
          "Position is added to the vector")
LG = PANEL_L_X + INNER + GUT

input_row(L, ghost=False)

y, h = R2
arrow_down(L + COL_W / 2, R1[0] + R1[1], y)
s.node(L, y, COL_W, h, "cat + p3", "the vector that enters attention", "pos", mono=True)
s.wrapped(LG, y + 28, "Position enters here, before attention begins.",
          GUT_W, 22, C["pos"]["text"], 700)

y, h = R3
fan(L + COL_W / 2, R2[0] + R2[1], y, [L + o + w / 2 for o, w in CHIP])
for (o, w), lab, kind in zip(CHIP, "QKV", ["qk", "qk", "v"]):
    s.node(L + o, y, w, h, lab, "shifted", kind)
s.wrapped(LG, y + 30, "All three projections inherit the position.", GUT_W, 22, MUTED)

y, h = R4
for o, w in CHIP:
    arrow_down(L + o + w / 2, R3[0] + R3[1], y)
s.node(L, y, COL_W, h, "routing and content", "both carry an absolute position", "plain")

takeaway(s, PANEL_L_X, TAKE[0], TAKE[1], "Position changes what a token is.", "token")

# ============================================================ RIGHT: RoPE
R = panel(s, PANEL_R_X, TOP, BOT, "ROTARY POSITIONAL EMBEDDINGS",
          "Position rotates the query and key")
RG = PANEL_R_X + INNER + GUT

input_row(R, ghost=True)

y, h = R2
arrow_down(R + BOX_W / 2, R1[0] + R1[1], y)      # the real flow bypasses the crossed-out addition
s.node(R, y, COL_W, h, "cat", "the vector that enters attention", "token", mono=True)
s.wrapped(RG, y + 28, "Nothing is added to the token vector.", GUT_W, 22, MUTED)

y, h = R3
fan(R + COL_W / 2, R2[0] + R2[1], y, [R + o + w / 2 for o, w in CHIP])
# the amber ring marks exactly what position touches: Q and K, never V
s.rect(R + CHIP[0][0] - 12, y - 14, (CHIP[1][0] + CHIP[1][1] + 12) - (CHIP[0][0] - 12), h + 28,
       r=22, fill=C["pos"]["fill"], stroke=C["pos"]["stroke"], sw=3, dash="9 7")
s.node(R + CHIP[0][0], y, CHIP[0][1], h, "Q", "rotated", "qk")
s.node(R + CHIP[1][0], y, CHIP[1][1], h, "K", "rotated", "qk")
s.node(R + CHIP[2][0], y, CHIP[2][1], h, "V", "not rotated", "v", sub_fill=C["v"]["text"])
s.wrapped(RG, y + 4, "Position enters here, inside attention, and only through Q and K.",
          GUT_W, 22, C["pos"]["text"], 700)

y, h = R4
for o, w in CHIP[:2]:
    arrow_down(R + o + w / 2, R3[0] + R3[1] + 14, y)
arrow_down(R + CHIP[2][0] + CHIP[2][1] / 2, R3[0] + R3[1], y,
           colour=C["v"]["stroke"], marker="aTeal")
s.node(R, y, 205, h, "where to look", "depends on m - n", "out")
s.node(R + CHIP[2][0] + CHIP[2][1] / 2 - 100, y, 200, h, "what to collect", "unchanged", "v",
       label_size=22)

takeaway(s, PANEL_R_X, TAKE[0], TAKE[1], "Position changes how two tokens compare.", "out")

footnote(s, BOT + 48, "Queries and keys decide which positions interact. Values carry the "
                      "content being retrieved, so they are left alone.")
emit(s, "rope-positioning-explained.svg")
