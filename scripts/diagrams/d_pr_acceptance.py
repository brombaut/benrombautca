"""LinearB's 8.1M PRs: acceptance rate by author, and the pickup delay.

The one chart among this post's figures. A value axis with horizontal bars does not
exist in frame.py and is not being added there: the helpers below are local, built on
the Svg primitives and the frame.py width constants only, the same arrangement
d_agent_spectrum.py uses for its local axis-with-bars layout.

Colour: frame.C is semantic (blue tokens, purple Q/K, teal V, amber the operation
under comparison, green the residual path) and none of that applies to PR acceptance.
Two series need two colours, so this picks the two neutral content hues, `token`
(blue) for human PRs and `qk` (purple) for AI PRs. Neither carries a pass/fail
valence the way `out` (green) or `pos` (amber) would, and the post makes no claim
about which author *should* win. Colour never carries the distinction alone: every
bar is named next to it and labelled with its own value.
"""
from svgkit import Svg, INK, MUTED, FAINT, EDGE, C, WARN, tw, shrink
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER)

POST = "ai-slop-phase-transition"

CW = PANEL_W - 2 * INNER          # content width inside a panel, 625

TOP, BOT = 200, 916
H = 1014

CAT_CAP = TOP + 148               # the category-axis caption
NAME_Y = [TOP + 206, TOP + 330]   # baseline of each bar's name
BAR_Y = [TOP + 222, TOP + 346]    # top of each bar
BAR_H = 74
AXIS_Y = BAR_Y[1] + BAR_H + 20    # the zero line / value axis
TICK_Y = AXIS_Y + 32              # tick labels
VAX_Y = AXIS_Y + 72               # value-axis title
GLOSS_Y = AXIS_Y + 126
TAKE_Y, TAKE_H = 822, 60

HUMAN, AI = C["token"], C["qk"]


def value_axis(s, x, vmax, ticks, title, top):
    """Zero line, dashed gridlines, tick labels and an axis title. Zero-anchored."""
    for t in ticks:
        gx = x + CW * t / vmax
        if t:
            s.path(f"M{gx:g} {top:g} V{AXIS_Y:g}", stroke=EDGE, sw=2, dash="5 8", cap="butt")
        lab = f"{t:g}"
        s.text(gx, TICK_Y, lab, 21, 400, FAINT, "middle")
    s.path(f"M{x:g} {top:g} V{AXIS_Y:g}", stroke=EDGE, sw=2.5, cap="butt")
    s.path(f"M{x:g} {AXIS_Y:g} H{x + CW:g}", stroke=EDGE, sw=2.5, cap="butt")
    sz = shrink(title, CW, 22, 400)
    s.text(x, VAX_Y, title, sz, 400, MUTED)


def bar(s, x, i, name, value, vmax, label, c, track=False):
    """One named horizontal bar carrying its own value label."""
    y, w = BAR_Y[i], CW * value / vmax
    ns = shrink(name, CW - tw(label, 34, 700) - 40, 27, 700)
    s.text(x, NAME_Y[i], name, ns, 700, INK)
    if track:
        s.rect(x, y, CW, BAR_H, r=12, fill=C["plain"]["fill"], stroke=EDGE, sw=2)
    s.rect(x, y, w, BAR_H, r=12, fill=c["fill"], stroke=c["stroke"], sw=2.5)
    # The value sits on the bar it describes, inside when there is room for it and
    # just past the end when there is not, so nobody reads it off a gridline.
    lw = tw(label, 34, 700)
    if lw + 36 <= w:
        s.text(x + w - 18, y + BAR_H / 2 + 12, label, 34, 700, c["text"], "end")
    else:
        if w + 18 + lw > CW:
            WARN.append(f"value label {label!r} runs past the plot: "
                        f"{w + 18 + lw:.0f} > {CW}")
        s.text(x + w + 18, y + BAR_H / 2 + 12, label, 34, 700, c["text"])


def chart(s, px, section, heading, rows, vmax, ticks, vtitle, gloss, take, track):
    x = panel(s, px, TOP, BOT, section, heading)
    s.text(x, CAT_CAP, "PR AUTHOR", 20, 700, FAINT, tracking=1.8)
    value_axis(s, x, vmax, ticks, vtitle, BAR_Y[0] - 14)
    for i, (name, value, label, c) in enumerate(rows):
        bar(s, x, i, name, value, vmax, label, c, track=track)
    s.wrapped(x, GLOSS_Y, gloss, CW, 22, MUTED)
    takeaway(s, px, TAKE_Y, TAKE_H, take, "plain")


s = page(H, "AI pull requests are accepted less, and wait longer",
         "LinearB's study of 8.1 million pull requests. Bars are grouped by who wrote the PR.")

chart(s, PANEL_L_X, "ACCEPTANCE", "Share of pull requests that get accepted",
      [("Human PRs", 84.4, "84.4%", HUMAN),
       ("AI PRs", 32.7, "32.7%", AI)],
      100, [0, 20, 40, 60, 80, 100],
      "share of that author's PRs accepted (%)",
      "The track behind each bar is every PR that author opened. Two of three AI PRs "
      "never land.",
      "Under half the human rate", True)

chart(s, PANEL_R_X, "PICKUP DELAY", "How long a pull request waits to be picked up",
      [("Human PRs", 1.0, "1.0x", HUMAN),
       ("Agentic PRs", 5.3, "5.3x", AI)],
      6, [0, 1, 2, 3, 4, 5, 6],
      "wait before pickup, in multiples of the human wait",
      "LinearB reports this one as a ratio, not a duration, so the human wait is the "
      "unit and there is no absolute scale.",
      "5.3x longer before a reviewer looks", False)

footnote(s, BOT + 46, "Acceptance is measured per author across all 8.1 million PRs. "
                      "The pickup figure is reported for agentic PRs specifically.")
emit(s, POST, "pr-acceptance-rates.svg")
