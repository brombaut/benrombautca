from svgkit import INK, MUTED, EDGE, CARD, C
from frame import page, footnote, emit, PANEL_L_X, PANEL_R_X, PANEL_W, INNER

POST = "ai-tools-q3-2026"

TOP, BOT = 200, 826
CARD_W = PANEL_R_X + PANEL_W - PANEL_L_X      # one card spanning both panel slots
X0 = PANEL_L_X + INNER + 236                  # timeline left edge, after the tool names
X1 = PANEL_L_X + CARD_W - INNER               # timeline right edge
MONTH_W = (X1 - X0) / 3
ROW0, ROW_H, PITCH = 318, 78, 118
GAP = 7                                       # half the gap left between adjacent bars
JOB_X = X0 + 2.5 * MONTH_W                    # the job change, drawn mid-September
H = BOT + 96

s = page(H, "The tools I used across Q3 2026",
         "Codex stopped when I changed jobs, and Claude Code is the default at the end.")
s.rect(PANEL_L_X, TOP, CARD_W, BOT - TOP, r=26, fill=CARD, stroke=EDGE, sw=2.5)

for i, month in enumerate(("JULY", "AUGUST", "SEPTEMBER")):
    x = X0 + i * MONTH_W
    s.text(x + GAP + 4, TOP + 62, month, 23, 700, MUTED, tracking=1.8)
    if i:
        s.path(f"M{x:g} {TOP + 34:g} V{BOT - 78:g}", stroke=EDGE, sw=2.5, cap="butt")

s.path(f"M{JOB_X:g} {ROW0 - 22:g} V{BOT - 74:g}", stroke=C["pos"]["stroke"], sw=2.5,
       dash="9 11", cap="butt")
s.text(JOB_X, BOT - 38, "changed jobs", 22, 700, C["pos"]["text"], "middle")


def row(i, name):
    y = ROW0 + i * PITCH
    s.text(PANEL_L_X + INNER, y + ROW_H / 2 + 9, name, 27, 700, INK)
    return y


def bar(y, a, b, label, sub, kind, dash=None):
    """A bar from timeline position a to b, each given in months from the start of July."""
    xa, xb = X0 + a * MONTH_W + GAP, X0 + b * MONTH_W - GAP
    s.node(xa, y, xb - xa, ROW_H, label, sub, kind, label_size=24, sub_size=19, dash=dash)


y = row(0, "Claude Code")
bar(y, 0, 2.5, "about even with Codex", "through work, and on my own subscription", "out")
bar(y, 2.5, 3, "the default", None, "out")

y = row(1, "Codex")
bar(y, 0, 2.5, "about even with Claude Code", "through work only", "token")
bar(y, 2.5, 3, "stopped", None, "ghost", dash="7 7")

y = row(2, "OpenCode")
bar(y, 0, 1, "made myself stay on it", None, "qk")
bar(y, 1, 3, "back to it now and then", "easy tasks, and trying cheaper models", "qk",
    dash="7 7")

y = row(3, "Chat models")
bar(y, 2, 3, "planning a vacation", None, "v")

footnote(s, BOT + 50, "Bars show when I was using a tool, not how much. "
                      "Dashed bars are occasional use or none.")
emit(s, POST, "tools-across-the-quarter.svg")
