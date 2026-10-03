from svgkit import Svg, INK, MUTED, EDGE, C, wrap
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER)

POST = "ai-tools-q1-2026"

TOP, BOT = 200, 1000
ROW0, ROW_H, PITCH = 352, 74, 112
SLOTS = 5                      # both panels share one five-slot band
BOX_W = 272                    # the item chip, identical in both panels
NOTE_X = INNER + BOX_W + 22    # reason column, offset from a panel's left edge
NOTE_W = PANEL_W - 2 * INNER - BOX_W - 22
TAKE_Y, TAKE_H = 906, 58
SEAM = (PANEL_L_X + PANEL_W + PANEL_R_X) / 2    # 800, the gap between the panels
STRIP_Y, STRIP_H = BOT + 40, 158
H = STRIP_Y + STRIP_H + 92

DROPPED = [
    ("Claude Code Radar", "a dashboard I built",
     "Fun to build, satisfying to watch. It never changed how I ran a session."),
    ("Kintsugi", "agent command center",
     "Very cool at first. The habit did not stick and I went back to plain tmux."),
    ("OpenCode", "model-per-role routing",
     "The cost idea is genuinely interesting. I kept drifting back to Claude Code."),
    ("Paper summaries repo", "for work reading",
     "Capture was easy. I almost never came back to read any of it."),
    ("Meeting and idea notes", "quick Claude Code chats",
     "Same shape as the papers. The retrieval habit never formed."),
]

KEPT = [
    ("tmux and Claude Code", "the main setup",
     "Several sessions at once, in the terminal. This is where the work happens."),
    ("Compacting early", "at natural break points",
     "I compact at a break instead of waiting for the context window to fill."),
    ("Handoff skill", "a markdown summary",
     "The next session starts with full context instead of re-reading the repo."),
]

s = page(H, "What stuck in Q1 2026, and what did not",
         "Everything I dropped was a thing to look at. Everything I kept was a change to how I work.")


def note(x, y, text, size=20, lh=26, fill=MUTED, weight=400):
    """Reason text, vertically centred against a row so short and long notes both sit right."""
    lines = wrap(text, NOTE_W, size, weight)
    y0 = y + ROW_H / 2 - (len(lines) - 1) * lh / 2 + size * 0.36
    for i, ln in enumerate(lines):
        s.text(x, y0 + i * lh, ln, size, weight, fill, "start")


def items(x, rows, kind, dash):
    """One chip per item plus its reason. Rows are centred in the shared five-slot band."""
    offset = (SLOTS - len(rows)) // 2
    for i, (label, sub, reason) in enumerate(rows):
        y = ROW0 + (i + offset) * PITCH
        s.node(x + INNER, y, BOX_W, ROW_H, label, sub, kind, label_size=25, dash=dash)
        note(x + NOTE_X, y, reason)


# ============================================================ LEFT: dropped
panel(s, PANEL_L_X, TOP, BOT, "TRIED AND DROPPED", "Five things, none still in use")
items(PANEL_L_X, DROPPED, "ghost", "7 7")
takeaway(s, PANEL_L_X, TAKE_Y, TAKE_H, "The ones that were fun to watch.", "ghost")

# ============================================================ RIGHT: kept
panel(s, PANEL_R_X, TOP, BOT, "KEPT", "Three things, all still in use")
items(PANEL_R_X, KEPT, "out", None)
takeaway(s, PANEL_R_X, TAKE_Y, TAKE_H, "The ones that changed how I work.", "out")

# ============================================================ the item that straddles
s.path(f"M{SEAM:g} {TOP + 30:g} V{STRIP_Y - 8:g}", stroke=EDGE, sw=2.5,
       dash="9 11", cap="butt")
s.rect(PANEL_L_X, STRIP_Y, PANEL_W * 2 + (PANEL_R_X - PANEL_L_X - PANEL_W), STRIP_H,
       r=26, fill="#fbfcfe", stroke=C["pos"]["stroke"], sw=2.5, dash="10 10")
s.text(PANEL_L_X + INNER, STRIP_Y + 48, "SITS ON THE LINE", 23, 700, MUTED, tracking=1.8)
# the seam continues through the strip, so the one undecided item is drawn sitting on it
s.path(f"M{SEAM:g} {STRIP_Y + 20:g} V{STRIP_Y + STRIP_H - 20:g}", stroke=EDGE, sw=2.5,
       dash="9 11", cap="butt")

BEAD_W, BEAD_H = 300, 74
s.node(SEAM - BEAD_W / 2, STRIP_Y + 52, BEAD_W, BEAD_H, "Beads", "issue tracking", "pos",
       label_size=28)

LN_X = PANEL_L_X + INNER
LN_W = SEAM - BEAD_W / 2 - 30 - LN_X
for i, ln in enumerate(wrap("Useful, and I am still in the trying-it-out phase.",
                            LN_W, 21, 400)):
    s.text(LN_X, STRIP_Y + 97 + i * 27, ln, 21, 400, INK)

RN_X = SEAM + BEAD_W / 2 + 30
RN_W = PANEL_R_X + PANEL_W - INNER - RN_X
for i, ln in enumerate(wrap("Keeping the pipeline full and tracking issues across clones "
                            "are real problems. I think they are growing pains.",
                            RN_W, 21, 400)):
    s.text(RN_X, STRIP_Y + 82 + i * 27, ln, 21, 400, INK)

footnote(s, STRIP_Y + STRIP_H + 52,
         "Beads is the one I cannot file yet: it changes how I work when it works, and "
         "I am still deciding whether it does.")
emit(s, POST, "q1-2026-what-stuck.svg")
