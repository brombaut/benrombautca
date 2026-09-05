from svgkit import Svg, INK, MUTED, FAINT, EDGE, ARROW, C
from frame import (page, panel, takeaway, footnote, emit,
                   PANEL_L_X, PANEL_R_X, PANEL_W, INNER, COL_W, GUT, GUT_W)

H = 1140
TOP, BOT = 200, 1028

s = page(H, "GQA keeps every query, but shares the keys and values",
         "The saving shows up in the KV cache during generation, not in training speed.")

ROWS = [330, 410, 490, 570]        # the four query heads
RH = 60
Q_W = 100
K_X, V_X, KV_CW = 214, 304, 80     # the key and value chips of one pair
BOX_X, BOX_W = 200, 198            # the container drawn around a shared pair
DIV = 678
TILE_Y, TILE_H, TILE_GAP = 740, 34, 10
TAKE = (938, 56)


def kv_pair(x, y, h, ksuffix, size=22):
    """K and V keep the colours they have in the RoPE diagram: K is a routing chip, V is content."""
    s.node(x + K_X, y, KV_CW, h, "K" + ksuffix, None, "qk", label_size=size)
    s.node(x + V_X, y, KV_CW, h, "V" + ksuffix, None, "v", label_size=size)


def heads(x, groups):
    """groups: list of (first_row, last_row, name); rows in one group share a single K/V pair."""
    for i, y in enumerate(ROWS):
        s.node(x, y, Q_W, RH, f"Q{i + 1}", None, "qk", label_size=26)
    for first, last, name in groups:
        top = ROWS[first]
        box_h = ROWS[last] + RH - top
        shared = last > first
        # both panels wrap each K/V pair in the same container; only its height differs
        if shared:
            s.rect(x + BOX_X, top, BOX_W, box_h, r=20, fill="#fbfcfe", stroke="#c8d3e2", sw=2.5)
            s.text(x + BOX_X + BOX_W / 2, top + 36, name, 22, 700, MUTED, "middle")
            kv_pair(x, top + 52, box_h - 76, "")
        else:
            s.rect(x + BOX_X, top - 6, BOX_W, RH + 12, r=20, fill="#fbfcfe",
                   stroke="#c8d3e2", sw=2.5)
            kv_pair(x, top, RH, name)
        # land each query on its own point of the target edge so arrowheads never collide
        span, n = box_h - 36, last - first + 1
        for j, r in enumerate(range(first, last + 1)):
            y0 = ROWS[r] + RH / 2
            y1 = top + 18 + span * (j + 0.5) / n
            x0 = x + Q_W
            x1 = x + BOX_X
            s.path(f"M{x0:g} {y0:g} C{x0 + 60:g} {y0:g} {x1 - 60:g} {y1:g} {x1:g} {y1:g}",
                   sw=3.5, marker="aGrey")


def cache(x, suffixes, big, big_fill):
    s.path(f"M{x:g} {DIV:g} H{x + COL_W + GUT_W + 20:g}", stroke=EDGE, sw=2.5, cap="butt")
    s.text(x, DIV + 40, "KV CACHE WHILE GENERATING", 21, 700, MUTED, tracking=1.6)
    s.text(x, TILE_Y + 38, big, 44, 700, big_fill)
    s.text(x, TILE_Y + 72, "cached per token", 21, 400, MUTED)
    for i, suf in enumerate(suffixes):
        kv_pair(x, TILE_Y + i * (TILE_H + TILE_GAP), TILE_H, suf, size=19)


# ============================================================ LEFT: standard MHA
L = panel(s, PANEL_L_X, TOP, BOT, "STANDARD MULTI-HEAD ATTENTION",
          "Four queries, four K/V pairs")
LG = PANEL_L_X + INNER + GUT

heads(L, [(i, i, str(i + 1)) for i in range(4)])
s.wrapped(LG, ROWS[1] + 12, "Every query head owns a private key and value head.",
          GUT_W, 22, MUTED)
cache(L, ["1", "2", "3", "4"], "4 sets", INK)
s.wrapped(LG, TILE_Y + 32, "Four sets are appended for every token generated.", GUT_W, 22, MUTED)
takeaway(s, PANEL_L_X, TAKE[0], TAKE[1], "Four query heads, four sets to cache.", "plain")

# ============================================================ RIGHT: GQA
R = panel(s, PANEL_R_X, TOP, BOT, "GROUPED-QUERY ATTENTION",
          "Four queries, two K/V pairs")
RG = PANEL_R_X + INNER + GUT

heads(R, [(0, 1, "group A"), (2, 3, "group B")])
s.wrapped(RG, ROWS[1] + 12, "Two query heads read the same keys and values, and still ask "
                            "different questions.", GUT_W, 22, MUTED)
cache(R, [" A", " B"], "2 sets", C["out"]["text"])
s.wrapped(RG, TILE_Y + 32, "Same four queries, half the cached state.",
          GUT_W, 22, C["out"]["text"], 700)
takeaway(s, PANEL_R_X, TAKE[0], TAKE[1], "Four query heads, two sets to cache.", "out")

footnote(s, BOT + 46, "Training expands the shared keys and values back to four heads, so GQA is "
                      "about cache size at inference, not training speed.")
emit(s, "gqa-kv-cache-explained.svg")
