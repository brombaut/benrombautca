"""The five context-compaction strategies applied to one shared message history.

The post's compaction section is already organized as five strategies, so the
layout is a grid: the input history drawn once down the left as chips, then one
column per strategy showing what that strategy does with each message, and three
footer rows for the properties that differ (who triggers it, what it costs, what
it loses).

frame.py only lays out two fixed panels, so the N-across row helper below is
local, built on the Svg primitives and the frame.py width constants only. Same
precedent as d_agent_spectrum.py and d_slop_families.py.
"""
from frame import page, footnote, emit, W, PANEL_L_X
from svgkit import INK, MUTED, EDGE, CARD, C, WARN, shrink, wrap

POST = "coding-agent-architectures"

# ---------------------------------------------------------------- geometry
X0 = PANEL_L_X                      # 70
X1 = W - PANEL_L_X                  # 1530
SPAN = X1 - X0                      # 1460

LBL_W = 264                         # the shared history column
LBL_GAP = 20
GAPX = 14
COLW = (SPAN - LBL_W - LBL_GAP - 4 * GAPX) // 5      # 224

HDR_NAME = 212                      # baseline of the first strategy-name line
RULE = 322
GRID_TOP = 344
PITCH = 48
CELL_H = 40
NROW = 10

FOOT_GAP = 16                       # between the grid and the footer rows
FOOT_PAD = 11                       # inner padding of a footer cell
FOOT_LH = 25
FOOT_SZ = 19


def col_x(i):
    return X0 + LBL_W + LBL_GAP + i * (COLW + GAPX)


def row_y(i):
    return GRID_TOP + i * PITCH


# ---------------------------------------------------------------- content
# The shared input history. Ten messages: a system prompt, the issue, then four
# action/observation pairs. Deliberately generic; every strategy in the post
# operates on a list shaped like this one.
HISTORY = [
    "system prompt",
    "the issue text",
    "act 1: grep",
    "obs 1: 200 lines",
    "act 2: read file",
    "obs 2: 400 lines",
    "act 3: edit",
    "obs 3: diff applied",
    "act 4: run tests",
    "obs 4: 3 failures",
]

KEPT = ("token", "kept")
STUB = ("ghost", "placeholder")
ELSE = ("ghost", "another node")

# Each strategy: the cells it puts against the ten messages. A ("span", a, b,
# label, sub) entry replaces rows a..b with one box, which is what summarizing
# actually does to a run of messages.
STRATS = [
    dict(
        name="No compaction",
        agents="mini-swe-agent",
        accent="pos",
        cells=[KEPT] * 10,
        decided="nobody; the list just grows",
        calls="none",
        loses="nothing, until the window overflows and the run dies",
    ),
    dict(
        name="Rule-based truncation",
        agents="SWE-agent, DARS-Agent",
        accent="ghost",
        cells=[KEPT, KEPT, KEPT, STUB, KEPT, STUB, KEPT, KEPT, KEPT, KEPT],
        decided="a fixed rule, on every step",
        calls="none; it is pure Python",
        loses="whole observations, all or nothing",
    ),
    dict(
        name="LLM summarization",
        agents="Aider, OpenHands, OpenCode",
        accent="qk",
        cells=[KEPT, ("span", 1, 6, "one summary", "six messages in")] + [KEPT] * 3,
        decided="a token threshold in the scaffold",
        calls="a summarizer call, often on a cheaper model",
        loses="detail, and whatever the summarizer judges wrong",
    ),
    dict(
        name="Structural isolation",
        agents="Prometheus",
        accent="out",
        cells=[KEPT, KEPT] + [ELSE] * 6 + [KEPT, KEPT],
        decided="the graph, at build time",
        calls="none; nothing is compacted",
        loses="nothing it needed, if the graph is drawn right",
    ),
    dict(
        name="LLM-initiated compaction",
        agents="Cline",
        accent="qk",
        cells=[KEPT, ("span", 1, 6, "one summary", "six messages in")] + [KEPT] * 3,
        decided="the LLM, mid-task, via a condense tool",
        calls="a condense call, when the LLM asks for one",
        loses="the same as summarizing, on the LLM's timing",
    ),
]

FOOT_ROWS = [
    ("Triggered by", "decided"),
    ("Extra LLM calls", "calls"),
    ("What it loses", "loses"),
]

NOTES = [
    ("Gemini CLI checks its own work.",
     "After summarizing it runs a verification probe, a self-correction turn that asks "
     "whether anything critical was dropped. No other agent validates its own compaction."),
    ("The three summarizers disagree.",
     "Aider overwrites the originals in place. OpenHands keeps the raw events beside the "
     "summary. OpenCode prunes verbose tool output first, then summarizes what is left."),
    ("Doing nothing is a real choice.",
     "mini-swe-agent never compacts. With step and cost limits in place, a bounded task "
     "finishes before the context window fills."),
]

TAKEAWAY = ("A rule cannot tell an irrelevant old observation from the one holding the key "
            "insight. An LLM can, and sometimes gets it wrong.")

FOOTNOTE = ("SWE-agent's rule keeps the first user message and the last five observations; "
            "the grid shows the last two, over a ten-message history.")


# ---------------------------------------------------------------- drawing
def strategy_header(s, i, st):
    x = col_x(i)
    c = C[st["accent"]]
    lines = wrap(st["name"], COLW, 24, 700)
    for j, ln in enumerate(lines):
        s.text(x, HDR_NAME + j * 30, ln, 24, 700, INK)
    y = HDR_NAME + len(lines) * 30 + 2
    for j, ln in enumerate(wrap(st["agents"], COLW, 19, 400)):
        s.text(x, y + j * 24, ln, 19, 400, MUTED)
    s.rect(x, RULE, COLW, 4, r=2, fill=c["stroke"])


def history_column(s):
    s.text(X0, HDR_NAME, "The same history", 24, 700, INK)
    sub = "ten messages, one run"
    s.text(X0, HDR_NAME + 30, sub, shrink(sub, LBL_W - 10, 19), 400, MUTED)
    s.rect(X0, RULE, LBL_W, 4, r=2, fill=EDGE)
    for i, msg in enumerate(HISTORY):
        s.node(X0, row_y(i), LBL_W, CELL_H, msg, kind="plain", label_size=20, r=12)


def grid(s):
    for i, st in enumerate(STRATS):
        x = col_x(i)
        r = 0                       # a span covers several rows, so walk, don't enumerate
        for cell in st["cells"]:
            if cell[0] == "span":
                _, a, b, label, sub = cell
                top = row_y(a)
                h = row_y(b) + CELL_H - top
                s.node(x, top, COLW, h, label, sub, kind="qk",
                       label_size=23, sub_size=18, r=12)
                r = b + 1
                continue
            kind, label = cell
            s.node(x, row_y(r), COLW, CELL_H, label, kind=kind, label_size=20, r=12,
                   dash="7 6" if kind == "ghost" else None)
            r += 1
        if r != NROW:
            print(f"  !! {st['name']} covers {r} rows, not {NROW}")


def footer(s, top):
    """Three property rows. Each row's height is the tallest wrapped cell in it."""
    y = top
    for title, key in FOOT_ROWS:
        counts = [len(wrap(st[key], COLW - 2 * FOOT_PAD, FOOT_SZ, 400)) for st in STRATS]
        h = max(counts) * FOOT_LH + 2 * FOOT_PAD
        ts = shrink(title, LBL_W - 8, 21, 700)
        s.text(X0 + LBL_W, y + FOOT_PAD + FOOT_SZ + 2, title, ts, 700, INK, "end")
        for i, st in enumerate(STRATS):
            x = col_x(i)
            s.rect(x, y, COLW, h, r=12, fill=CARD, stroke=EDGE, sw=2)
            s.wrapped(x + FOOT_PAD, y + FOOT_PAD + FOOT_SZ, st[key],
                      COLW - 2 * FOOT_PAD, FOOT_SZ, MUTED, lh=FOOT_LH)
        y += h + 12
    return y


def note_card(s, top):
    sub = (SPAN - 56 - 2 * 24) // 3
    counts = [len(wrap(what, sub, 20, 400)) for _, what in NOTES]
    h = 64 + 26 + max(counts) * 25 + 14
    s.rect(X0, top, SPAN, h, r=20, fill=CARD, stroke=EDGE, sw=2.5)
    s.text(X0 + 28, top + 42, "What the five columns do not show", 24, 700, INK)
    for i, (who, what) in enumerate(NOTES):
        x = X0 + 28 + i * (sub + 24)
        s.text(x, top + 82, who, 21, 700, INK)
        s.wrapped(x, top + 108, what, sub, 20, MUTED, lh=25)
    return top + h


def takeaway_bar(s, top):
    c = C["out"]
    h = 62
    s.rect(X0, top, SPAN, h, r=16, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    sz = shrink(TAKEAWAY, SPAN - 60, 27, 700)
    s.text(W / 2, top + h / 2 + sz * 0.36, TAKEAWAY, sz, 700, c["text"], "middle")
    return top + h


# ---------------------------------------------------------------- assembly
def build():
    # Lay the page out twice: once to measure the stack, once to draw it at the
    # height the content actually needs.
    probe = page(10, "x", "y")
    foot_end = footer(probe, row_y(NROW - 1) + CELL_H + FOOT_GAP)
    note_end = note_card(probe, foot_end + 10)
    take_end = takeaway_bar(probe, note_end + 18)
    h = int(take_end + 96)
    # The probe measured every string the real pass measures again, so drop its
    # duplicate warnings rather than printing each one twice.
    WARN.clear()

    s = page(h, "Five ways to compact a coding agent's history",
             "Rows are messages, columns are strategies. Every column starts from the "
             "same ten-message history on the left.")
    history_column(s)
    for i, st in enumerate(STRATS):
        strategy_header(s, i, st)
    grid(s)
    foot_end = footer(s, row_y(NROW - 1) + CELL_H + FOOT_GAP)
    note_end = note_card(s, foot_end + 10)
    take_end = takeaway_bar(s, note_end + 18)
    footnote(s, take_end + 46, FOOTNOTE)
    emit(s, POST, "compaction-strategies.svg")


build()
