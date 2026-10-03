from svgkit import Svg, INK, MUTED, FAINT, ARROW, C, wrap, shrink
from frame import (page, panel, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER, COL_W, GUT, GUT_W)

POST = "ai-tools-q2-2026"

H = 1210
TOP, BOT = 200, 1110

s = page(H, "Where the review gate sits",
         "Same pipeline either way. The only thing that moves is the gate.")

# ---- chain geometry, identical in both panels ----
BOX_W, BOX_H = 220, 62
CHAIN_OFF = 110                  # centre of the stage column, from the panel's inner left
ROWS = (330, 510, 690, 870)      # task, plan, implement, merge
GAPS = (451, 631, 811)           # the three slots between stages
PILL_W, PILL_H = 250, 56
TRACK_OFF, TRACK_W = 250, 140    # the debt track, right of the stage column
TRACK_TOP, BAR_H, BAR_PITCH = 700, 20, 34
LABEL_Y = 925
TAKE_Y, TAKE_H = 980, 86

STAGES = ("task", "plan", "implement", "merged")
AMBER, PURPLE = C["pos"], C["qk"]


def stage_column(cx):
    for y, name in zip(ROWS, STAGES):
        s.node(cx - BOX_W / 2, y, BOX_W, BOX_H, name, None, "plain", label_size=26)


def link(y0, y1, cx):
    s.path(f"M{cx:g} {y0:g} V{y1:g}", sw=4, marker="aGrey")


def gate(cx, slot, sub, kind="pos"):
    """A pill sitting across the flow line, wider than the stages so it reads as a gate."""
    y = GAPS[slot] - PILL_H / 2
    s.node(cx - PILL_W / 2, y, PILL_W, PILL_H, "human review gate", sub, kind,
           label_size=23, sub_size=19, r=28,
           sub_fill=C[kind]["text"] if kind == "pos" else None)
    return y


def track(x0, widths, kind, label):
    c = C[kind]
    for i, w in enumerate(widths):
        y = TRACK_TOP + i * BAR_PITCH
        s.rect(x0, y, w, BAR_H, r=7, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    for i, ln in enumerate(wrap(label, PANEL_W - 2 * INNER - TRACK_OFF, 19, 700)):
        s.text(x0, LABEL_Y + i * 25, ln, 19, 700, c["text"])


def takeaway2(x, text, kind):
    """Two-line takeaway bar: the given wording is too long for a single legible line."""
    c = C[kind]
    w = PANEL_W - 2 * INNER
    s.rect(x + INNER, TAKE_Y, w, TAKE_H, r=14, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    size = 27
    lines = wrap(text, w - 44, size, 700)
    while len(lines) > 2 and size > 20:
        size -= 1
        lines = wrap(text, w - 44, size, 700)
    y0 = TAKE_Y + TAKE_H / 2 + size * 0.36 - (len(lines) - 1) * (size + 9) / 2
    for i, ln in enumerate(lines):
        s.text(x + PANEL_W / 2, y0 + i * (size + 9), ln, size, 700, c["text"], "middle")


# ============================================================ LEFT: late 2025
L = panel(s, PANEL_L_X, TOP, BOT, "LATE 2025",
          "The gate sits after the implementation")
LC, LG, LT = L + CHAIN_OFF, L + GUT, L + TRACK_OFF

stage_column(LC)
link(ROWS[0] + BOX_H, ROWS[1], LC)
link(ROWS[1] + BOX_H, ROWS[2], LC)
gy = gate(LC, 2, "read every line")
link(ROWS[2] + BOX_H, gy, LC)
link(gy + PILL_H, ROWS[3], LC)
track(LT, [96] * 6, "ghost", "mental model keeps up")

s.wrapped(LG, 622, "No gate here yet.", GUT_W, 22, FAINT)
s.wrapped(LG, 790, "Nothing merges until I have read the implementation.",
          GUT_W, 22, AMBER["text"], 700)
takeaway2(PANEL_L_X, "The job was writing correct code.", "token")

# ============================================================ RIGHT: Q2 2026
R = panel(s, PANEL_R_X, TOP, BOT, "Q2 2026",
          "The gate sits after the plan")
RC, RG, RT = R + CHAIN_OFF, R + GUT, R + TRACK_OFF

stage_column(RC)
link(ROWS[0] + BOX_H, ROWS[1], RC)
gy2 = gate(RC, 1, "review the plan")
link(ROWS[1] + BOX_H, gy2, RC)
link(gy2 + PILL_H, ROWS[2], RC)
ry = GAPS[2] - 26
s.node(RC - BOX_W / 2, ry, BOX_W, 52, "code review", "lighter", "ghost",
       label_size=22, sub_size=18, r=26)
link(ROWS[2] + BOX_H, ry, RC)
link(ry + 52, ROWS[3], RC)
track(RT, [26, 49, 72, 95, 118, 140], "qk", "comprehension debt")

s.wrapped(RG, 520, "I review the plan, the intended files, the expected shape of the "
                   "change, and the assumptions.", GUT_W, 22, AMBER["text"], 700)
s.wrapped(RG, 790, "The code review still happens. It no longer carries the weight.",
          GUT_W, 22, MUTED)
takeaway2(PANEL_R_X, "The job is shaping the task so the agent writes correct code.", "pos")

footnote(s, BOT + 46, "If the plan is wrong, the implementation will be wrong in a way that "
                      "looks locally reasonable.")
emit(s, POST, "review-gate-placement.svg")
