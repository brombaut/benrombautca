"""The workflow is the product: the loop around the agent, with each workflow pinned.

The post's last line names the loop: "planning, delegation, verification, memory,
summarization, and knowing when to stop". So the six stages are drawn as a ring in
that order, the agent sits in the middle as the one part of the system I did not
build, and every workflow the post describes is pinned outside the ring at the stage
it serves. The one stage with nothing pinned to it is drawn as a ghost, because the
post says outright that it has no solution for it.

A ring or cycle layout does not exist in frame.py, and is not added there: the
helpers below are local on purpose, built on the Svg primitives and the frame.py
width constants only, the same way d_agent_spectrum.py and d_slop_families.py keep
their own layouts local. Stage positions and the arc endpoints between them are
computed from the ellipse, and every arc is trimmed until both of its ends clear the
boxes it runs between, so an arrowhead can never land on a label.
"""
import math

from frame import emit, footnote, page
from svgkit import C, FAINT, MUTED, WARN, shrink, tw, wrap

POST = "ai-tools-q2-2026"

H = 1380

# ---------------------------------------------------------------- ring geometry
CX, CY = 800, 740          # ring centre
RX, RY = 330, 340          # the stages sit on this ellipse
BW, BH = 270, 92           # stage box
PAD = 14                   # clearance an arc must keep from a box

# angle, label, sub-label, palette key. Clockwise from the top, in the post's order.
STAGES = [
    (-90, "Planning", "shape the task", "token"),
    (-30, "Delegation", "hand it to an agent", "token"),
    (30, "Verification", "verify intent", "token"),
    (90, "Memory", "project state", "token"),
    (150, "Summarization", "a recoverable thread", "token"),
    (210, "Knowing when to stop", "the open problem", "ghost"),
]

AMBER = C["pos"]
RECTS = []                 # (name, x, y, w, h) for the overlap check


def reg(name, x, y, w, h):
    RECTS.append((name, x, y, w, h))
    return x, y, w, h


def ring(theta):
    r = math.radians(theta)
    return CX + RX * math.cos(r), CY + RY * math.sin(r)


def box_of(theta):
    cx, cy = ring(theta)
    return cx - BW / 2, cy - BH / 2, BW, BH


def outside(pt, rect, pad):
    x, y, w, h = rect
    return not (x - pad <= pt[0] <= x + w + pad and y - pad <= pt[1] <= y + h + pad)


def clear(start, step, rect):
    """Walk away from `start` until the ellipse point clears `rect`."""
    theta = start
    for _ in range(1200):
        if outside(ring(theta), rect, PAD):
            return theta
        theta += step
    return theta


def arc(theta_a, theta_b):
    """Arc along the ring from one stage to the next, trimmed clear of both boxes."""
    a = clear(theta_a, 0.25, box_of(theta_a))
    b = clear(theta_b, -0.25, box_of(theta_b))
    (x1, y1), (x2, y2) = ring(a), ring(b)
    s.path(f"M{x1:.1f} {y1:.1f} A{RX:g} {RY:g} 0 0 1 {x2:.1f} {y2:.1f}",
           sw=4, marker="aGrey")
    return (a + b) / 2


def block(x, y, head, body, colour, anchor="start", max_w=250,
          hsize=23, bsize=21, lh=29, name=""):
    """A pinned annotation: a bold workflow name over wrapped body copy."""
    hsize = shrink(head, max_w, hsize, 700)
    lines = wrap(body, max_w, bsize)
    s.text(x, y, head, hsize, 700, colour, anchor)
    for i, ln in enumerate(lines):
        s.text(x, y + 34 + i * lh, ln, bsize, 400, MUTED, anchor)
    w = max([tw(head, hsize, 700)] + [tw(ln, bsize) for ln in lines])
    x0 = {"start": x, "end": x - w, "middle": x - w / 2}[anchor]
    top, bot = y - hsize, y + 34 + (len(lines) - 1) * lh + bsize * 0.3
    return reg(name or head, x0, top, w, bot - top)


def leader(x1, y1, x2, y2, colour=FAINT, marker="aFaint"):
    s.path(f"M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}", stroke=colour, sw=3,
           marker=marker, dash="7 8")


# ---------------------------------------------------------------- page
s = page(H, "The workflow is the product",
         "The loop around the agent, and the workflow pinned to each stage of it")

# the six stages, then the arcs between them
for theta, label, sub, kind in STAGES:
    x, y, w, h = reg(label, *box_of(theta))
    s.node(x, y, w, h, label, sub, kind, label_size=25, sub_size=20)

mids = {}
for i, (theta, label, _, _) in enumerate(STAGES):
    nxt = STAGES[(i + 1) % len(STAGES)][0]
    mids[label] = arc(theta, nxt if nxt > theta else nxt + 360)

# the agent, in the middle of its own loop
AX, AY, AW, AH = reg("agent", CX - 140, CY - 48, 280, 96)
s.node(AX, AY, AW, AH, "the agent", "only one part of the system", "plain",
       label_size=27, sub_size=21)

# ---------------------------------------------------------------- pinned workflows
PL = box_of(-90)       # planning, top
DE = box_of(-30)       # delegation, upper right
VE = box_of(30)        # verification, lower right
ME = box_of(90)        # memory, bottom
SU = box_of(150)       # summarization, lower left
ST = box_of(210)       # knowing when to stop, upper left

TOKEN = C["token"]["text"]
LCOL, W_R = 80, 1520

b = block(CX, 238, "research-junshi and research-checkin",
          "A daily digest of related papers, nearby ideas and possible next steps, "
          "built from the project's current state.",
          TOKEN, "middle", max_w=980, name="research workflow")
leader(CX, b[1] + b[3] + 18, CX, PL[1] - 8)

b = block(W_R, 495, "the tool split",
          "Codex for light and medium engineering work. Claude Code for heavier work "
          "and the skills I built around it. Chat for thinking outside the repo.",
          TOKEN, "end", name="tool split")
leader(b[0] - 16, DE[1] + BH / 2, DE[0] + BW + 10, DE[1] + BH / 2)

b = block(W_R, 835, "the planning pass",
          "The agent investigates the codebase and writes a plan. I review the "
          "intended files, the shape of the change and the assumptions.",
          TOKEN, "end", name="planning pass")
leader(b[0] - 16, VE[1] + BH / 2, VE[0] + BW + 10, VE[1] + BH / 2)

b = block(CX, 1200, "the weekly summary",
          "The dailies rolled up into a multi-day view by day and project. A durable "
          "record instead of terminal scrollback.",
          TOKEN, "middle", max_w=980, name="weekly summary")
leader(CX, b[1] - 18, CX, ME[1] + BH + 8)

b = block(LCOL, 835, "the daily summary",
          "Scans the day's session transcripts into a recap: projects touched, "
          "accomplishments, trouble spots, follow-up work.",
          TOKEN, name="daily summary")
leader(b[0] + b[2] + 16, SU[1] + BH / 2, SU[0] - 10, SU[1] + BH / 2)

b = block(LCOL, 495, "nothing covers this one",
          "The AI Vampire. Starting work costs almost nothing, so stopping is the "
          "harder action. I can tell when it is happening. Awareness is not a boundary.",
          C["ghost"]["text"], name="no workflow")
leader(b[0] + b[2] + 16, ST[1] + BH / 2, ST[0] - 10, ST[1] + BH / 2)

# the compaction boundary: the seam where one session ends and the next plans again
px, py = ring(mids["Knowing when to stop"])
nx, ny = RY * math.cos(math.radians(mids["Knowing when to stop"])), \
    RX * math.sin(math.radians(mids["Knowing when to stop"]))
nl = math.hypot(nx, ny)
nx, ny = nx / nl, ny / nl
s.path(f"M{px - nx * 19:.1f} {py - ny * 19:.1f} L{px + nx * 19:.1f} {py + ny * 19:.1f}",
       stroke=AMBER["stroke"], sw=4.5)
b = block(LCOL, 300, "the handoff doc",
          "What context needs to survive compaction.",
          AMBER["text"], name="handoff doc")
leader(b[0] + b[2] + 20, b[1] + b[3] - 4, px - 44, py - 24,
       AMBER["stroke"], "aAmber")

footnote(s, H - 50, "Five of the six stages have a workflow I actually use. "
                    "The sixth is the one I have no answer for.")

# ---------------------------------------------------------------- collision check
for i in range(len(RECTS)):
    for j in range(i + 1, len(RECTS)):
        (n1, x1, y1, w1, h1), (n2, x2, y2, w2, h2) = RECTS[i], RECTS[j]
        if (x1 - 4 < x2 + w2 + 4 and x2 - 4 < x1 + w1 + 4
                and y1 - 4 < y2 + h2 + 4 and y2 - 4 < y1 + h1 + 4):
            WARN.append(f"{n1!r} overlaps {n2!r}")

emit(s, POST, "workflow-is-the-product.svg")
