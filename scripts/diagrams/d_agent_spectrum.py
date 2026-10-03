"""The autonomy spectrum: all 13 coding agents placed by control flow.

A horizontal axis with one column per control-flow band. This layout (an axis with
banded columns of chips) does not exist in frame.py, so the helpers below are local:
they are built on the Svg primitives and the frame.py width constants only.
"""
from svgkit import Svg, INK, MUTED, FAINT, EDGE, ARROW, CARD, C, tw, wrap, shrink
from frame import page, footnote, emit, W, PANEL_L_X

POST = "coding-agent-architectures"

X0 = PANEL_L_X                  # 70
X1 = W - PANEL_L_X              # 1530
SPAN = X1 - X0                  # 1460
GAPX = 16
COLW = (SPAN - 4 * GAPX) // 5   # 279

AXIS = 250                      # the spectrum line
RULE = 384                      # coloured rule under each band header
CHIP_Y = 402
CHIP_H, CHIP_GAP = 92, 12
CHIP_STRIDE = CHIP_H + CHIP_GAP

NOTE_CARD = 1156
NOTE_H = 134
TAKE_Y = 1322
TAKE_H = 62
H = 1458

MAX_TOOLS = 37                  # Moatless Tools, the longest bar

# Band order runs left to right from "nothing decides what comes next" to
# "the system searches over alternatives". Prometheus sits with AutoCodeRover in
# the phased band: the post calls it a LangGraph state machine whose nodes bind
# only the tools they need, which is phase separation enforced by a graph.
BANDS = [
    dict(kind="plain", label="Fixed pipeline", desc="No loop. Stages run once.",
         note="Agentless samples ~40 patches independently and majority-votes. "
              "No feedback, so a bad localization wastes every one of them.",
         agents=[("Agentless", "0", 0, "1 on the Anthropic path", False)]),
    dict(kind="token", label="User-driven loop", desc="The user picks the next step.",
         note="The LLM's job is to emit edit blocks in one of 13 formats. A lint "
              "and test reflection loop runs, but the user still chooses what happens next.",
         agents=[("Aider", "0", 0, "the user drives the loop", True)]),
    dict(kind="v", label="Phased loop", desc="The scaffold fixes the stages.",
         note="AutoCodeRover enforces the split in code: the patch agent cannot "
              "import the search backend. Prometheus binds 1-10 tools per graph node. "
              "Neither can interleave search and editing.",
         agents=[("AutoCodeRover", "8", 8, "all read-only", True),
                 ("Prometheus", "17", 17, "1-10 per graph node", False)]),
    dict(kind="qk", label="Sequential loop", desc="The LLM picks every step.",
         note=None,
         agents=[("mini-swe-agent", "1", 1, "bash, which does anything", True),
                 ("SWE-agent", "3", 3, "~34 across all bundles", False),
                 ("OpenHands", "9", 9, "+ MCP", False),
                 ("Gemini CLI", "17", 17, "+ MCP", False),
                 ("OpenCode", "18", 18, "+ MCP + plugins", False),
                 ("Codex CLI", "~20", 20, "+ MCP", False),
                 ("Cline", "27", 27, "+ MCP, and condense", False)]),
    dict(kind="pos", label="Tree search", desc="The system compares branches.",
         note="DARS replays the container to reach a branch point, so it branches "
              "only at edits. Moatless keeps edits virtual in shadow mode, which is "
              "what makes branching cheap.",
         agents=[("DARS-Agent", "~15", 15, "at edit actions only", False),
                 ("Moatless Tools", "37", 37, "~15 active at a time", False)]),
]

CAVEATS = [
    ("Aider, 0 tools.", "The user drives the loop, so the LLM never needs one to be useful."),
    ("AutoCodeRover, 8 tools.", "All eight are read-only search. None of them can change the repo."),
    ("mini-swe-agent, 1 tool.", "It is bash, and bash can run anything the container can."),
]


def col_x(i):
    return X0 + i * (COLW + GAPX)


def spectrum_axis(s):
    """The horizontal line, its end labels, and a tick per band."""
    s.path(f"M{X0} {AXIS} H{X1 - 6}", stroke=ARROW, sw=4, marker="aGrey")
    s.text(X0, AXIS - 22, "fixed stages", 22, 700, FAINT)
    s.text(X1, AXIS - 22, "search over alternatives", 22, 700, FAINT, "end")
    for i, band in enumerate(BANDS):
        cx = col_x(i) + COLW / 2
        c = C[band["kind"]]
        s.circle(cx, AXIS, 10, fill=c["stroke"])
        s.path(f"M{cx:g} {AXIS + 14} V{RULE - 96}", stroke=c["stroke"], sw=2.5, dash="6 7")


def band_header(s, i, band):
    x, c = col_x(i), C[band["kind"]]
    n = f"{len(band['agents'])} of 13"
    ls = shrink(band["label"], COLW - tw(n, 20, 700) - 18, 25, 700)
    s.text(x, RULE - 62, band["label"], ls, 700, INK)
    s.text(x + COLW, RULE - 62, n, 20, 700, c["stroke"], "end")
    for j, ln in enumerate(wrap(band["desc"], COLW, 20, 400)):
        s.text(x, RULE - 32 + j * 25, ln, 20, 400, MUTED)
    s.rect(x, RULE, COLW, 4, r=2, fill=c["stroke"])


def chip(s, x, y, name, badge, count, qual, flagged, kind):
    """One agent: name, its tool-count badge, the qualifier, and a count bar."""
    c = C[kind]
    s.rect(x, y, COLW, CHIP_H, r=14, fill=c["fill"], stroke=c["stroke"], sw=2.5,
           dash="8 7" if flagged else None)
    bw = tw(badge, 26, 700)
    ns = shrink(name, COLW - 32 - bw - 16, 24, 700)
    s.text(x + 16, y + 34, name, ns, 700, c["text"])
    s.text(x + COLW - 16, y + 35, badge, 26, 700, c["stroke"], "end")
    qs = shrink(qual, COLW - 32, 19, 400)
    s.text(x + 16, y + 60, qual, qs, 400, MUTED)
    track = COLW - 32
    s.rect(x + 16, y + 72, track, 7, r=3.5, fill=EDGE)
    if count:
        s.rect(x + 16, y + 72, track * count / MAX_TOOLS, 7, r=3.5, fill=c["stroke"])


def caveat_card(s):
    s.rect(X0, NOTE_CARD, SPAN, NOTE_H, r=20, fill=CARD, stroke=EDGE, sw=2.5)
    s.text(X0 + 28, NOTE_CARD + 42,
           "Dashed chips: where the tool count says the opposite of what it looks like",
           24, 700, INK)
    sub = (SPAN - 56 - 2 * 20) // 3
    for i, (who, what) in enumerate(CAVEATS):
        cx = X0 + 28 + i * (sub + 20)
        s.text(cx, NOTE_CARD + 82, who, 21, 700, INK)
        s.wrapped(cx, NOTE_CARD + 108, what, sub, 20, MUTED, lh=25)


def takeaway_bar(s):
    c = C["out"]
    s.rect(X0, TAKE_Y, SPAN, TAKE_H, r=16, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    txt = ("The question is not whether a design is an agent, "
           "but where it sits on this axis and what that position costs.")
    sz = shrink(txt, SPAN - 60, 27, 700)
    s.text(W / 2, TAKE_Y + TAKE_H / 2 + sz * 0.36, txt, sz, 700, c["text"], "middle")


s = page(H, "\"Agent\" is a spectrum: 13 coding agents by control flow",
         "Columns are control-flow bands, left to right. The number and bar on each chip are "
         "the tools the LLM can call.")

spectrum_axis(s)

for i, band in enumerate(BANDS):
    band_header(s, i, band)
    x = col_x(i)
    for j, (name, badge, count, qual, flagged) in enumerate(band["agents"]):
        chip(s, x, CHIP_Y + j * CHIP_STRIDE, name, badge, count, qual, flagged, band["kind"])
    if band["note"]:
        ny = CHIP_Y + len(band["agents"]) * CHIP_STRIDE + 14
        s.wrapped(x, ny, band["note"], COLW, 20, MUTED, lh=27)

caveat_card(s)
takeaway_bar(s)
footnote(s, H - 46, "Counts are LLM-callable tools, bars scaled to Moatless Tools' 37. "
                    "A longer bar means more tools, not more autonomy.")
emit(s, POST, "agent-autonomy-spectrum.svg")
