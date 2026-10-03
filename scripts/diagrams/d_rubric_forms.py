from svgkit import Svg, INK, MUTED, FAINT, EDGE, C, wrap
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER, COL_W, GUT, GUT_W)

POST = "from-checklists-to-prose-verdicts"

H = 1350
TOP, BOT = 200, 1246

# One skeleton, used by both panels: the shared axis, what the evaluator fills in,
# and what comes out. Only the middle and bottom stages change form.
S1_LBL, AXIS_Y, AXIS_H = 340, 356, 76
DIV_1 = 470
S2_LBL, S2_Y = 508, 526
CARD_H, CARD_GAP = 112, 18
S2_H = 3 * CARD_H + 2 * CARD_GAP          # 372; the prose card matches it exactly
DIV_2 = S2_Y + S2_H + 38                  # 936
S3_LBL, OUT_Y, OUT_H = 974, 990, 86
UNDER = OUT_Y + OUT_H + 32
TAKE_Y, TAKE_H = 1150, 56

s = page(H, "The same axis, scored two ways",
         "One Astropy WCS patch, one architectural axis. The prose form is the one I "
         "shipped; the checklist is reconstructed.")


def stage(x, label, y):
    s.text(x, y, label, 21, 700, MUTED, tracking=1.6)


def divider(px, y):
    s.path(f"M{px + INNER:g} {y:g} H{px + PANEL_W - INNER:g}", stroke=EDGE, sw=2.5, cap="butt")


def axis_chip(x):
    """Identical in both panels: the one thing that does not move."""
    s.node(x, AXIS_Y, COL_W, AXIS_H, "wrapper_delegation_integrity",
           "the three-step expand, delegate, contract pattern",
           "token", label_size=22, sub_size=19, mono=True)


def chip(x, y, w, label, kind, size=18):
    c = C[kind]
    s.rect(x, y, w, 30, r=9, fill=c["fill"], stroke=c["stroke"], sw=2)
    s.text(x + w / 2, y + 21, label, size, 700, c["text"], "middle", mono=True)


def mark(x, y, ok, colour):
    """Vector tick or cross, so nothing depends on glyph coverage."""
    if ok:
        s.path(f"M{x:g} {y + 2:g} l 6 7 l 11 -14", stroke=colour, sw=3.5)
    else:
        s.path(f"M{x:g} {y - 6:g} l 15 15 M{x + 15:g} {y - 6:g} l -15 15",
               stroke=colour, sw=3.5)


def verdict_pill(x, y, label, ok):
    c = C["out"] if ok else C["pos"]
    w = 88
    s.rect(x, y, w, 30, r=15, fill=c["fill"], stroke=c["stroke"], sw=2)
    mark(x + 13, y + 15, ok, c["stroke"])
    s.text(x + w - 13, y + 21, label, 18, 700, c["text"], "end")


def item(x, y, ident, weight, metric, ok):
    s.rect(x, y, COL_W, CARD_H, r=14, fill="#fbfcfe", stroke="#c8d3e2", sw=2.5)
    chip(x + 14, y + 13, 66, ident, "token")
    s.text(x + 92, y + 34, f"weight {weight}", 18, 400, FAINT)
    verdict_pill(x + COL_W - 14 - 88, y + 13, "PASS" if ok else "FAIL", ok)
    s.wrapped(x + 14, y + 66, metric, COL_W - 28, 19, MUTED, lh=25)


def result(x, label, sub, under, kind):
    s.node(x, OUT_Y, COL_W, OUT_H, label, sub, kind, label_size=40, sub_size=20)
    s.text(x, UNDER, under, 20, 400, FAINT)


# ============================================================ LEFT: itemized checklist
L = panel(s, PANEL_L_X, TOP, BOT, "ITEMIZED CHECKLIST",
          "How many boxes did the patch check?")
LG = PANEL_L_X + INNER + GUT

stage(L, "THE AXIS", S1_LBL)
axis_chip(L)
divider(PANEL_L_X, DIV_1)

stage(L, "WHAT THE EVALUATOR FILLS IN", S2_LBL)
item(L, S2_Y, "WDI1", 3,
     "All changes stay inside world_to_pixel_values and its helpers.", True)
item(L, S2_Y + CARD_H + CARD_GAP, "WDI2", 2,
     "Delegation call and output contraction left unmodified.", True)
item(L, S2_Y + 2 * (CARD_H + CARD_GAP), "WDI3", 2,
     "Dropped dimensions read through the helper the rubric named.", False)
s.wrapped(LG, S2_Y + 36, "Every item is a binary call against its own threshold, then weighted.",
          GUT_W, 21, MUTED)
divider(PANEL_L_X, DIV_2)

stage(L, "WHAT COMES OUT", S3_LBL)
result(L, "0.71", "weighted pass rate", "5 of 7 points, comparable across patches", "pos")
s.wrapped(LG, OUT_Y + 14, "WDI3 names a mechanism, not a property. An equivalent route "
                          "scores as a miss.", GUT_W, 21, C["pos"]["text"], 700, lh=28)
takeaway(s, PANEL_L_X, TAKE_Y, TAKE_H, "Precise, and some of that precision is false.", "pos")

# ============================================================ RIGHT: prose verdict
R = panel(s, PANEL_R_X, TOP, BOT, "PROSE ASSESSMENT",
          "Did the patch preserve the property?")
RG = PANEL_R_X + INNER + GUT

stage(R, "THE AXIS", S1_LBL)
axis_chip(R)
divider(PANEL_R_X, DIV_1)

stage(R, "WHAT THE EVALUATOR FILLS IN", S2_LBL)
s.rect(R, S2_Y, COL_W, S2_H, r=14, fill="#fbfcfe", stroke="#c8d3e2", sw=2.5)
chip(R + 14, S2_Y + 13, 104, "PRIMARY", "v")
s.text(R + COL_W - 14, S2_Y + 34, "no items, no thresholds", 18, 400, FAINT, "end")
s.wrapped(R + 14, S2_Y + 70,
          "Maintains the three-step delegation pattern. Only the expansion step is "
          "modified; the delegation call and the output contraction are untouched. "
          "Dropped-dimension values are computed on the fly through an existing "
          "helper, so no new state is introduced. The mechanism differs from the one "
          "the checklist itemized, and it reaches the same structural guarantee.",
          COL_W - 28, 21, INK, lh=28)
s.wrapped(RG, S2_Y + 36, "One judgment about the whole axis, with a priority in place of a "
                         "weight.", GUT_W, 21, MUTED)
divider(PANEL_R_X, DIV_2)

stage(R, "WHAT COMES OUT", S3_LBL)
result(R, "High", "architectural conformance", "architecture only, not a correctness claim",
       "out")
s.wrapped(RG, OUT_Y + 14, "An equivalent route to the same property, not a miss.",
          GUT_W, 21, C["out"]["text"], 700, lh=28)
takeaway(s, PANEL_R_X, TAKE_Y, TAKE_H, "Better reasoning, some distinctions flattened.", "out")

footnote(s, BOT + 46, "High covers everything from solid to exemplary, so the top tier stops "
                      "separating. That is the cost the hybrid is meant to buy back.")
emit(s, POST, "rubric-forms-compared.svg")
