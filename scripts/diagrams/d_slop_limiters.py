from svgkit import Svg, INK, MUTED, FAINT, ARROW, C, tw, shrink
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER)

POST = "ai-slop-phase-transition"

H = 1400
TOP, BOT = 200, 1294

CW = PANEL_W - 2 * INNER          # content width inside a panel
GREEN, AMBER = C["out"]["stroke"], C["pos"]["stroke"]

INTENT = (318, 66, 250)           # y, h, w
GY0, GH, PITCH = 428, 62, 90      # first gate y, gate height, gate pitch
NGATE = 6
COMMIT = (1000, 70, 320)          # y, h, w
GLOSS_Y = 1112
TAKE = (1192, 54)

GATES = [
    ("typing cost",           "verbosity was self-limiting", "no cost"),
    ("boredom",               "a repetition detector",       "never bored"),
    ("fatigue",               "a stopping rule",             "never tired"),
    ("shame",                 "a pre-commit hook",           "no shame"),
    ("knowing the codebase",  "the deduplicator",            "no memory"),
    ("consequence ownership", "your tests, your pain",       "no stake"),
]

s = page(H, "Boredom was a quality control",
         "The same path from intent to committed code. Only the gates on it differ.")


def gate_y(i):
    return GY0 + i * PITCH


# The path runs down the middle of every bar, so each bar's text keeps a clear
# corridor around it: label left of the spine, gloss right of it. One size for
# every row, so the rhythm does not wobble.
SLOT = CW / 2 - 24 - 30
LSZ = min(shrink(g[0], SLOT, 24, 700) for g in GATES)
RSZ = min(min(shrink(g[1], SLOT, 21), shrink(g[2], SLOT, 21)) for g in GATES)


def bar(x, y, label, right, kind, dashed=False):
    """A full-width gate bar: bold label on the left, its gloss on the right."""
    c = C[kind]
    s.rect(x, y, CW, GH, r=14, fill=c["fill"], stroke=c["stroke"], sw=2.5,
           dash="9 8" if dashed else None)
    s.text(x + 24, y + GH / 2 + 8, label, LSZ, 700, c["text"])
    s.text(x + CW - 24, y + GH / 2 + 8, right, RSZ, 400,
           FAINT if dashed else MUTED, "end")


def spine(xc, y0, y1, marker=None):
    s.path(f"M{xc:g} {y0:g} V{y1:g}", stroke=GREEN, sw=6, marker=marker)


def ends(x, xc):
    s.node(xc - INTENT[2] / 2, INTENT[0], INTENT[2], INTENT[1], "intent", None, "out")
    s.node(xc - COMMIT[2] / 2, COMMIT[0], COMMIT[2], COMMIT[1], "committed code",
           None, "out", label_size=24)


def build(px, section, heading, gated, gloss, take, take_kind):
    x = panel(s, px, TOP, BOT, section, heading)
    xc = x + CW / 2
    if gated:
        # The path is interrupted: it stops at each gate and resumes below it.
        spine(xc, INTENT[0] + INTENT[1], GY0)
        for i in range(NGATE - 1):
            spine(xc, gate_y(i) + GH, gate_y(i + 1))
        spine(xc, gate_y(NGATE - 1) + GH, COMMIT[0], marker="aGreen")
        for i, (label, g, _) in enumerate(GATES):
            bar(x, gate_y(i), label, g, "pos")
    else:
        for i, (label, _, note) in enumerate(GATES):
            bar(x, gate_y(i), label, note, "ghost", dashed=True)
        # One unbroken run: nothing on the path stops it.
        spine(xc, INTENT[0] + INTENT[1], COMMIT[0], marker="aGreen")
    ends(x, xc)
    s.wrapped(x, GLOSS_Y, gloss, CW, 22, MUTED)
    takeaway(s, px, TAKE[0], TAKE[1], take, take_kind)


build(PANEL_L_X, "HUMAN PRODUCER", "Six limiters, each a gate on the path", True,
      "Too few tests, missing docs, copy-paste instead of careful abstraction.",
      "Fails by omission", "out")

build(PANEL_R_X, "LLM PRODUCER", "The same path, every gate gone", False,
      "Too much code, too many tests, logic rewritten from scratch, hedging "
      "compiled into control flow.",
      "Fails by commission", "pos")

footnote(s, BOT + 46, "In humans, high output correlated with the seniority to know "
                      "better, which capped a junior's blast radius. That went too.")
emit(s, POST, "quality-limiters-bundled-with-the-producer.svg")
