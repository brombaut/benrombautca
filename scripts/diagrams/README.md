# Blog Diagrams

Python generators for the explanatory SVG diagrams in blog posts. Each diagram is
described in code, measured against real font metrics, and rendered to PNG.

These exist because the hand-written SVGs they replaced kept overflowing: labels ran
outside their boxes, arrowheads landed on top of text. Here every string is measured
against the actual TTF before a box is sized, and anything that still does not fit
prints a warning at build time.

## Requirements

- Python 3 with `Pillow` (text measurement) and `PyGObject` (rendering)
- `librsvg` reachable through GdkPixbuf: `gir1.2-gdkpixbuf-2.0`, `librsvg2-common`
- `fontconfig` (`fc-match`) plus the Noto Sans and DejaVu Sans Mono families

Fonts are resolved with `fc-match`, not hardcoded paths, so the metrics used for
measurement are the ones librsvg will actually render with.

## Regenerating

```bash
python3 scripts/diagrams/build.py          # every diagram: SVG + PNG
python3 scripts/diagrams/d_rope.py         # just one
```

Output goes to `src/blog/content/images/<post-slug>/`, overwriting both the `.svg`
and the `.png`. The SVGs are plain shapes and text with no embedded rasters, so they
stay hand-editable; regenerating discards hand edits.

Watch the build output. A line starting with `!!` means a string did not fit its
container and the layout needs adjusting:

```
d_gqa.py
  !! footnote overflows: 1487 > 1460
```

## Files

| File | Purpose |
| --- | --- |
| `svgkit.py` | Engine: font measurement (`tw`, `wrap`, `shrink`), primitives, `node()`, overflow warnings |
| `frame.py` | House style: palette, page frame, panels, gutter, takeaway bars, footnote, `emit()` |
| `render.py` | SVG to PNG via librsvg/GdkPixbuf at 1.5x |
| `build.py` | Runs every `d_*.py` |
| `d_rope.py` | RoPE vs learned absolute positions |
| `d_gqa.py` | Grouped-query attention and the KV cache |
| `d_norm.py` | Pre-norm vs post-norm residual paths |

## Adding a diagram

Copy the `d_*.py` closest in shape to what you need. The three cover different
layouts: `d_rope.py` is a staged top-to-bottom flow, `d_gqa.py` is a repeated-row
comparison with a quantity payoff, `d_norm.py` is a graph with a branch and a
highlighted residual path.

The shared skeleton is a title and subtitle, two comparison panels, and a footnote.
Inside each panel: a section label, a heading, a content column, an annotation
gutter on the right (`GUT`, `GUT_W`) that keeps notes clear of the diagram, and a
takeaway bar at the bottom.

Rules worth keeping:

- Size boxes from measured text (`node()` auto-shrinks; `wrapped()` auto-wraps).
- Both panels should share a skeleton so only the meaningful difference moves.
- Semantic colours, defined in `frame.C`: blue tokens, purple Q/K, teal V, amber for
  the operation being compared, green for the residual/identity path.
- Draw symbols as vectors, not glyphs. `plus()` exists because `⊕` coverage is not
  guaranteed and a missing glyph silently breaks measurement.
- Land converging arrows on distinct points of a shared edge so arrowheads never stack.

## Checking the result

Diagrams display around 800px wide on the blog. Downscale and read them at that size
before committing, and confirm the post's markdown still resolves:

```bash
grep -o 'images/[a-z0-9/-]*\.png' src/blog/content/sources_md/<post>.md
```
