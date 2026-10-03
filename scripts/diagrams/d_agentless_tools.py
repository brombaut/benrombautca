"""Agentless's hardcoded tool loop: a tool-use loop whose results are a constant.

Layout is the house two-panel frame with one addition, kept local to this file: the
content column is a single vertical stack (`row`) with the loop's return path routed
down a narrow channel to its left (`loop_back`), which leaves the annotation gutter
free for notes. Both panels run the same five rows, so the only things that move are
what the middle row does, what the result row contains, and what happens after the
loop. The literal tool result is set in mono so it reads as a constant, and the
column is sized so that string fits at the same size in both panels.
"""
from svgkit import Svg, INK, MUTED, FAINT, ARROW, C
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER)

POST = "coding-agent-architectures"

H = 1200
TOP, BOT = 200, 1100

s = page(H, "Agentless's hardcoded tool loop",
         "Both loops issue tool calls. Only one of them executes anything.")

# -- content column -------------------------------------------------------
# 70 channel + 364 column + 20 gap + 171 gutter = 625, the panel's inner width.
BOFF, BW = 70, 364          # box column: offset from the panel's content edge, width
ROFF = 24                   # the loop's return channel
# The frame's GUT/GUT_W assume a narrower content column than the mono result
# string needs, so this figure carries its own gutter: 70 + 364 + 20 + 171 = 625,
# the panel's inner width.
GOFF, GW = 454, 171
MONO = 20                   # one size for every mono label, so constants look alike

A = (340, 80)               # the model
B = (464, 74)               # the tool call
Cc = (582, 88)              # what answers it
D = (714, 88)               # the tool result
DIV = 846                   # "after the loop" divider
E = (876, 92)               # what the edits become
TAKE = (1016, 56)

AMBER, GREEN = C["pos"]["stroke"], C["out"]["stroke"]


def row(bx, slot, label, sub, kind, mono=False, dash=None):
    y, h = slot
    s.node(bx, y, BW, h, label, sub, kind, label_size=MONO if mono else 25,
           mono=mono, dash=dash)
    return y + h


def down(bx, frm, to):
    """One straight hop down the stack, centred on the column."""
    cx = bx + BW / 2
    s.path(f"M{cx:g} {frm[0] + frm[1]:g} V{to[0]:g}", sw=4, marker="aGrey")


def loop_back(bx, rx):
    """Result row -> back up the left channel -> into the model's left edge."""
    y_from, y_to = D[0] + D[1] / 2, A[0] + A[1] / 2
    s.path(f"M{bx:g} {y_from:g} H{rx:g} V{y_to:g} H{bx:g}", sw=4, marker="aGrey")
    s.circle(bx, y_from, 7, fill=ARROW)


def divider(bx):
    s.text(bx, DIV - 14, "AFTER THE LOOP", 20, 700, FAINT, tracking=1.6)
    s.path(f"M{bx:g} {DIV:g} H{bx + BW:g}", stroke="#dbe3ef", sw=2.5, dash="9 8")


def gnote(gx, y, text, fill=MUTED, weight=400):
    s.wrapped(gx, y, text, GW, 19, fill, weight, lh=25)


def build(px, section, heading, right):
    x = panel(s, px, TOP, BOT, section, heading)
    bx, rx, gx = x + BOFF, x + ROFF, x + GOFF

    row(bx, A, "LLM", "picks the next edit", "token")
    row(bx, B, "str_replace_editor", "tool call", "qk", mono=True)
    if right:
        row(bx, Cc, "no execution", "the edit is appended to a list", "ghost", dash="9 7")
        row(bx, D, '"File is successfully edited."', "tool result, every time",
            "pos", mono=True)
        row(bx, E, "apply_edits(...)", "every collected edit, applied at once",
            "out", mono=True)
    else:
        row(bx, Cc, "the environment", "applies the edit to the file", "v")
        row(bx, D, "the edited file", "tool result, read from disk", "pos")
        row(bx, E, "nothing left to apply", "the file changed as the loop ran", "out")

    down(bx, A, B)
    down(bx, B, Cc)
    down(bx, Cc, D)
    divider(bx)
    loop_back(bx, rx)

    if right:
        gnote(gx, A[0] + 54, "Ten iterations at most, and it ends as soon as the "
                             "model stops calling the tool.")
        gnote(gx, D[0] + 22, "The same string comes back whatever the call asked "
                             "for.", C["pos"]["text"], 700)
        gnote(gx, E[0] + 30, "The edits land on the file only here, all at once, "
                             "after the model has stopped.")
        takeaway(s, px, TAKE[0], TAKE[1],
                 "Structured output extraction disguised as tool use.", "pos")
    else:
        gnote(gx, A[0] + 54, "Every iteration starts from what the last one "
                             "actually did.")
        gnote(gx, D[0] + 22, "The model reads real file state before its next "
                             "call.", C["pos"]["text"], 700)
        gnote(gx, E[0] + 30, "Each call already changed the file, so there is "
                             "nothing to replay.")
        takeaway(s, px, TAKE[0], TAKE[1],
                 "The model's next call answers to real file state.", "out")


build(PANEL_L_X, "A REAL TOOL LOOP", "The environment answers the call", False)
build(PANEL_R_X, "AGENTLESS, ANTHROPIC PATH", "A constant answers the call", True)

footnote(s, BOT + 46, "Only Agentless's Anthropic code path does this. Its default "
                      "path registers no tools at all, so there is no loop to fake.")
emit(s, POST, "agentless-hardcoded-tool-loop.svg")
