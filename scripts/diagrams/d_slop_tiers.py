"""The three tiers of AI code quality, drawn as two overlapping regions.

The post names three tiers: traditional smells, gray smells, AI-specific slop. It
does *not* describe them as concentric rings. Gray smells are defined as "patterns
that predate AI but appear disproportionately in AI output", so that tier belongs to
both of the things the post contrasts: what predates AI, and what is distinctive to
AI output. The honest geometry is therefore two regions that overlap on the middle
tier, not three boxes inside one another. Each tier is a card; the regions are
rounded outlines drawn around the cards they contain, and the gray card is the only
one inside both.

No nested-region helper exists in frame.py, and none is added there: the helpers
below are local on purpose, the same call `d_slop_families.py` makes for its grid.
"""
from frame import page, footnote, emit
from svgkit import INK, MUTED, FAINT, EDGE, CARD, C, WARN, tw, shrink, wrap

POST = "ai-slop-phase-transition"

# ---------------------------------------------------------------- geometry
COL_X = [96, 575, 1054]
COL_W = 449
RIGHT = COL_X[2] + COL_W            # 1503
LEFT = COL_X[0]

RPAD = 22                           # how far a region stands off its cards
CARD_TOP = 300
CARD_H = 644
CARD_BOT = CARD_TOP + CARD_H

# The two regions. Each spans two adjacent columns, so they overlap on column 1.
# Their top and bottom edges are deliberately offset from each other, so inside
# the overlap you see two outlines rather than one merged box.
REGIONS = [
    # (label, first col, last col, top, bottom, label y, anchor, colour kind)
    ("PREDATES AI", 0, 1, 214, CARD_BOT + 40, 248, "start", "ghost"),
    ("DISTINCTIVE TO AI OUTPUT", 1, 2, 234, CARD_BOT + 20, 282, "end", "qk"),
]

PAD = 26                            # card inner margin
Y_KICK = 46
Y_NAME = 90
Y_DEF = 128
DEF_LH = 28
DEF_SIZE = 21
SUB_GAP = 40                        # above a sub-label
CHIP_H = 44
CHIP_PITCH = 54
BOX_H = 70

TAKE_Y = CARD_BOT + 86
TAKE_H = 66
H = TAKE_Y + TAKE_H + 78

# ---------------------------------------------------------------- content
# tier: (kind, kicker, name, definition, accent box, blocks, closing note)
# a block is (sub-label, [(chip label, chip value)])
TIERS = [
    dict(
        kind="ghost",
        kicker="TIER 1",
        name="Traditional smells",
        definition="The same ones we have always had. How the code was produced "
                   "does not change what they are.",
        box=None,
        blocks=[("WHAT THE TIER IS", [("old patterns, old detection", "")])],
        note="AI-focused tools bundle traditional smell detection alongside their "
             "AI-specific rules, because practitioners found AI makes the old "
             "problems worse.",
    ),
    dict(
        kind="pos",
        kicker="TIER 2",
        name="Gray smells",
        definition="Patterns that predate AI but appear disproportionately in AI "
                   "output.",
        box=("109 of 575 rules", "the gray zone, cataloged across 42 tools"),
        blocks=[
            ("RATE VS HUMAN REFERENCE SOLUTIONS", [
                ("unused imports", "2.8x"),
                ("broad exception handlers", "2.1x"),
            ]),
            ("GRAY RULES, BY TOOLS FLAGGING THEM", [
                ("swallowed exceptions", "18"),
                ("unused declarations", "12"),
                ("broad / bare except", "10"),
            ]),
        ],
        note=None,
    ),
    dict(
        kind="qk",
        kicker="TIER 3",
        name="AI-specific slop",
        definition="A genuinely new category of defect, distinctive to AI.",
        box=None,
        blocks=[("WHAT IT LOOKS LIKE", [
            ("narrator comments", ""),
            ("hallucinated imports", ""),
            ("cross-language contamination", ""),
            ("fake-done stubs", ""),
        ])],
        note="A rate limiter that just returns True is not an incomplete TODO. It "
             "is an executable success path, and everything downstream behaves as "
             "if the limit exists.",
    ),
]

s = page(H, "Three tiers of AI code quality",
         "Gray smells are old patterns at new rates, so the tiers overlap rather than nest")

# One chip text size across every card, so the rhythm does not wobble between
# columns. Values are measured first, since they take the space the label gets.
CHIP_W = COL_W - 2 * PAD
_VAL_SZ = 23
_LBL_SZ = 22
for t in TIERS:
    for _, chips in t["blocks"]:
        for lbl, val in chips:
            vw = tw(val, _VAL_SZ, 700) + 18 if val else 0
            _LBL_SZ = min(_LBL_SZ, shrink(lbl, CHIP_W - 28 - vw, _LBL_SZ, 600))


def chip(x, y, label, value, kind):
    c = C[kind]
    s.rect(x, y, CHIP_W, CHIP_H, r=12, fill=c["fill"], stroke=c["stroke"], sw=2)
    s.text(x + 16, y + CHIP_H / 2 + 7, label, _LBL_SZ, 600, c["text"])
    if value:
        s.text(x + CHIP_W - 16, y + CHIP_H / 2 + 8, value, _VAL_SZ, 700, c["text"], "end")


def card(i, t):
    """Draw one tier card and return the y its content ran to."""
    x, top = COL_X[i], CARD_TOP
    c = C[t["kind"]]
    s.rect(x, top, COL_W, CARD_H, r=20, fill=CARD, stroke=c["stroke"], sw=2.5)
    # a colour bar along the top edge, so the tier reads at half size
    s.rect(x + 20, top + 12, COL_W - 40, 8, r=4, fill=c["stroke"])

    cx, avail = x + PAD, COL_W - 2 * PAD
    s.text(cx, top + Y_KICK, t["kicker"], 20, 700, FAINT, tracking=2.0)
    s.text(cx, top + Y_NAME, t["name"], shrink(t["name"], avail, 30, 700), 700, INK)

    lines = wrap(t["definition"], avail, DEF_SIZE, 400)
    for j, ln in enumerate(lines):
        s.text(cx, top + Y_DEF + j * DEF_LH, ln, DEF_SIZE, 400, MUTED)
    y = top + Y_DEF + len(lines) * DEF_LH - 8

    if t["box"]:
        label, sub = t["box"]
        y += 18
        s.node(cx, y, avail, BOX_H, label, sub, t["kind"], label_size=27, sub_size=19)
        y += BOX_H

    for sub, chips in t["blocks"]:
        y += SUB_GAP
        s.text(cx, y, sub, shrink(sub, avail, 18, 700), 700, FAINT, tracking=1.4)
        y += 14
        for lbl, val in chips:
            chip(cx, y, lbl, val, t["kind"])
            y += CHIP_PITCH
        y -= CHIP_PITCH - CHIP_H

    if t["note"]:
        y += 26
        for j, ln in enumerate(wrap(t["note"], avail, 20, 400)):
            s.text(cx, y + 16 + j * 26, ln, 20, 400, MUTED)
        y += 16 + len(wrap(t["note"], avail, 20, 400)) * 26 - 8

    # A card is a region too: its content must not escape it.
    if y > top + CARD_H - 14:
        WARN.append(f"card {t['name']!r} content runs to {y:.0f} > {top + CARD_H - 14:.0f}")
    return y


def region(label, c0, c1, top, bottom, ly, anchor, kind):
    col = C[kind]["stroke"]
    # the ghost stroke is too light to read as a label at half size
    lab_col = MUTED if kind == "ghost" else col
    x0 = COL_X[c0] - RPAD
    x1 = COL_X[c1] + COL_W + RPAD
    s.rect(x0, top, x1 - x0, bottom - top, r=30, fill="none", stroke=col, sw=3,
           dash="2 0")
    lx = x0 + RPAD if anchor == "start" else x1 - RPAD
    sz = shrink(label, x1 - x0 - 2 * RPAD, 22, 700)
    s.text(lx, ly, label, sz, 700, lab_col, anchor, tracking=2.2)
    # the cards this region claims must sit inside it
    if COL_X[c0] < x0 or COL_X[c1] + COL_W > x1 or CARD_TOP < top or CARD_BOT > bottom:
        WARN.append(f"region {label!r} does not contain its cards")


def takeaway_bar(y, h, text, kind):
    c = C[kind]
    s.rect(LEFT - RPAD, y, (RIGHT + RPAD) - (LEFT - RPAD), h, r=16,
           fill=c["fill"], stroke=c["stroke"], sw=2.5)
    w = (RIGHT + RPAD) - (LEFT - RPAD) - 48
    sz = shrink(text, w, 27, 700)
    s.text((LEFT - RPAD + RIGHT + RPAD) / 2, y + h / 2 + sz * 0.36, text, sz, 700,
           c["text"], "middle")


def build():
    # the overlap, shaded first so the two region outlines draw on top of it
    ov_x0 = COL_X[1] - RPAD
    ov_x1 = COL_X[1] + COL_W + RPAD
    s.rect(ov_x0, REGIONS[1][3], ov_x1 - ov_x0, REGIONS[0][4] - REGIONS[1][3], r=28,
           fill="#f1f4fa", stroke="none", sw=0)
    for r in REGIONS:
        region(*r)
    ov = "both regions claim this tier"
    osz = shrink(ov, ov_x1 - ov_x0 - 24, 19, 400)
    s.text((ov_x0 + ov_x1) / 2, CARD_BOT + 36, ov, osz, 400, FAINT, "middle")

    for i, t in enumerate(TIERS):
        card(i, t)

    takeaway_bar(TAKE_Y, TAKE_H,
                 "A useful quality tool cannot only target the new stuff", "pos")
    footnote(s, H - 38,
             "Rates are measured against human-written reference solutions for the "
             "same tasks. Tool counts come from a survey of 70+ AI quality tools.")
    emit(s, POST, "three-tiers-of-smells.svg")


if __name__ == "__main__":
    build()
