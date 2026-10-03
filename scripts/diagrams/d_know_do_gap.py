"""The know-vs-do gap: one model, two workflows, the same fork taken differently.

The post's biggest surprise is that Claude Code generated both the rubrics and the
patches, and the patches did not reliably match the architectural ideal the rubrics
described. The stated cause is a difference in workflow behaviour: rubric generation
"naturally involved deep architectural reconnaissance", patch generation "could still
lapse into implementation search".

So the figure is two panels over one skeleton, in the shape of d_norm.py: the same
starting point, the same fork with the same two options, and only which option is
taken moving between panels. The not-taken option stays on the page as a ghost, which
is what makes the gap visible rather than asserted.

The fork-with-a-ghosted-alternative is not in frame.py, so `fork` and the step-card
helpers below are local on purpose; they are built on Svg primitives and the frame.py
constants only.
"""
from svgkit import INK, MUTED, FAINT, EDGE, C, tw
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER, COL_W, GUT, GUT_W)

POST = "from-checklists-to-prose-verdicts"

H = 1668
TOP, BOT = 200, 1548

# One skeleton for both panels: the shared start, the shared fork, what the workflow
# does, and what comes out. Only the taken branch and the step contents change.
S1_LBL, START_Y, START_H = 340, 356, 80
DIV_1 = 474

S2_LBL, FORK_Y, FORK_H = 512, 530, 54
OPT_X_OFF, OPT_W, OPT_H, OPT_GAP = 62, COL_W - 62, 82, 22
OPT_Y = [628, 628 + OPT_H + OPT_GAP]      # 628, 732
SPINE_OFF = [42, 20]                      # one spine per branch, left of the option boxes
DIV_2 = 858

S3_LBL, STEP_Y, STEP_H, STEP_GAP = 896, 912, 88, 14
DIV_3 = STEP_Y + 3 * STEP_H + 2 * STEP_GAP + 38     # 1238

S4_LBL, OUT_Y, OUT_H = 1276, 1292, 90
UNDER = OUT_Y + OUT_H + 32
TAKE_Y, TAKE_H = 1452, 56

RECON, SEARCH = "v", "pos"

s = page(H, "Know versus do: one model, two workflows",
         "Claude Code wrote both the rubrics and the patches. Only one workflow did "
         "the reconnaissance.")


def stage(x, label, y):
    s.text(x, y, label, 21, 700, MUTED, tracking=1.6)


def divider(px, y):
    s.path(f"M{px + INNER:g} {y:g} H{px + PANEL_W - INNER:g}", stroke=EDGE, sw=2.5, cap="butt")


def start_card(x):
    """Identical in both panels: the thing that does not move."""
    s.node(x, START_Y, COL_W, START_H, "one issue, one codebase, one model",
           "Claude Code on both sides of the pipeline", "token",
           label_size=23, sub_size=19)


def fork(x):
    """The shared decision point, stated the same way in both panels."""
    s.node(x, FORK_Y, COL_W, FORK_H, "open the affected area", None, "plain", label_size=23)


def option(x, i, label, sub, taken, kind):
    """One of the two branches. Taken: coloured, solid arrow. Not taken: ghosted.

    Each branch leaves the fork box at its own point on the shared bottom edge and
    runs down its own spine, so no two connectors share a segment and no two
    arrowheads stack.
    """
    ox, oy = x + OPT_X_OFF, OPT_Y[i]
    spine = x + SPINE_OFF[i]
    mid = oy + OPT_H / 2
    leave_x = x + COL_W / 2 - 38 * i
    turn_y = FORK_Y + FORK_H + 16 + 16 * i
    d = f"M{leave_x:g} {FORK_Y + FORK_H:g} V{turn_y:g} H{spine:g} V{mid:g} H{ox:g}"
    if taken:
        s.path(d, stroke=C[kind]["stroke"], sw=4,
               marker={"v": "aTeal", "pos": "aAmber"}[kind])
        s.node(ox, oy, OPT_W, OPT_H, label, sub, kind, label_size=25, sub_size=20)
    else:
        s.path(d, stroke=C["ghost"]["stroke"], sw=3, dash="9 9", marker="aFaint")
        s.node(ox, oy, OPT_W, OPT_H, label, sub, "ghost", label_size=25, sub_size=20,
               dash="8 8", sub_fill=C["ghost"]["text"])
        ly = oy - 11 if i == 0 else oy + OPT_H + 27
        s.text(ox + OPT_W - 2, ly, "not taken", 18, 700, FAINT, "end")


def branches(x, taken):
    """Both options, in the same order, in both panels. Only `taken` changes."""
    option(x, 0, "reconnaissance first", "map the pattern, then write",
           taken == 0, RECON)
    option(x, 1, "implementation search", "find a change that works",
           taken == 1, SEARCH)


def step(x, i, title, detail, kind):
    y = STEP_Y + i * (STEP_H + STEP_GAP)
    s.rect(x, y, COL_W, STEP_H, r=14, fill="#fbfcfe", stroke="#c8d3e2", sw=2.5)
    s.rect(x, y + 14, 5, STEP_H - 28, r=3, fill=C[kind]["stroke"])
    s.text(x + 22, y + 34, f"{i + 1}", 19, 700, FAINT)
    s.text(x + 48, y + 34, title, 21, 700, INK)
    s.wrapped(x + 48, y + 62, detail, COL_W - 66, 19, MUTED, lh=25)


def result(x, label, sub, under, kind):
    s.node(x, OUT_Y, COL_W, OUT_H, label, sub, kind, label_size=34, sub_size=20)
    s.text(x, UNDER, under, 20, 400, FAINT)


# ======================================================= LEFT: rubric generation
L = panel(s, PANEL_L_X, TOP, BOT, "RUBRIC GENERATION",
          "What does the architecture look like here?")
LG = PANEL_L_X + INNER + GUT

stage(L, "THE SHARED START", S1_LBL)
start_card(L)
divider(PANEL_L_X, DIV_1)

stage(L, "WHERE THEY DIVERGE", S2_LBL)
fork(L)
branches(L, taken=0)
s.wrapped(LG, OPT_Y[0] + 30, "Describing the architecture requires exploring it. This "
                             "workflow explores by construction.",
          GUT_W, 21, C[RECON]["text"], 700, lh=28)
divider(PANEL_L_X, DIV_2)

stage(L, "WHAT THE WORKFLOW DOES", S3_LBL)
step(L, 0, "Explore the codebase",
     "Read the wrapper, the delegation call, the layers around it.", RECON)
step(L, 1, "Name the structural property",
     "Expand, delegate, contract. The pattern a patch has to preserve.", RECON)
step(L, 2, "Commit it to the rubric",
     "The axis, its priority, the baseline and how it was measured.", RECON)
s.wrapped(LG, STEP_Y + 34, "Deep architectural reconnaissance, because the output is a "
                           "description of the architecture.", GUT_W, 21, MUTED, lh=28)
divider(PANEL_L_X, DIV_3)

stage(L, "WHAT COMES OUT", S4_LBL)
result(L, "a rubric", "the right architectural move, written down",
       "expand, delegate, contract", RECON)
takeaway(s, PANEL_L_X, TAKE_Y, TAKE_H, "The model can describe the move.", RECON)

# ======================================================= RIGHT: patch generation
R = panel(s, PANEL_R_X, TOP, BOT, "PATCH GENERATION",
          "What change makes this issue go away?")
RG = PANEL_R_X + INNER + GUT

stage(R, "THE SHARED START", S1_LBL)
start_card(R)
divider(PANEL_R_X, DIV_1)

stage(R, "WHERE THEY DIVERGE", S2_LBL)
fork(R)
branches(R, taken=1)
s.wrapped(RG, OPT_Y[0] + 30, "Nothing in the task forces that exploration, so this workflow "
                             "can lapse into search.",
          GUT_W, 21, C[SEARCH]["text"], 700, lh=28)
divider(PANEL_R_X, DIV_2)

stage(R, "WHAT THE WORKFLOW DOES", S3_LBL)
step(R, 0, "Locate the failing behaviour",
     "Find the code path that produces the wrong result.", SEARCH)
step(R, 1, "Search for a change that works",
     "Candidate edits, judged by whether the issue goes away.", SEARCH)
step(R, 2, "Write the patch",
     "No pass that asks which existing mechanism to extend.", SEARCH)
s.wrapped(RG, STEP_Y + 34, "The same reconnaissance is available here. It just is not "
                           "where the workflow starts.", GUT_W, 21, MUTED, lh=28)
divider(PANEL_R_X, DIV_3)

stage(R, "WHAT COMES OUT", S4_LBL)
result(R, "a patch", "that need not match the move the rubric named",
       "scored by the rubric the same model wrote", SEARCH)
takeaway(s, PANEL_R_X, TAKE_Y, TAKE_H, "It does not reliably take it.", SEARCH)

footnote(s, BOT + 46, "The fix was one sentence in the patch-generation prompt: understand "
                      "the patterns in the affected area before implementing.")
emit(s, POST, "know-vs-do-gap.svg")
