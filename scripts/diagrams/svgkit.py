"""Tiny SVG builder with real text measurement, so boxes always fit their text."""
import os
import subprocess
from PIL import ImageFont
from xml.sax.saxutils import escape


def _font_file(spec, fallback):
    """Ask fontconfig for the file it would use for `spec`.

    The SVGs name their fonts as "Noto Sans, sans-serif" and librsvg resolves that
    through fontconfig too, so going through fc-match keeps what we *measure* here
    identical to what actually gets *rendered*. Falls back to a Debian/Ubuntu path.
    """
    try:
        p = subprocess.run(["fc-match", "-f", "%{file}", spec],
                           capture_output=True, text=True, timeout=5)
        path = p.stdout.strip()
        if p.returncode == 0 and path and os.path.exists(path):
            return path
    except (OSError, subprocess.SubprocessError):
        pass
    return fallback


REG = _font_file("Noto Sans", "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf")
BLD = _font_file("Noto Sans:bold", "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf")
MNO = _font_file("DejaVu Sans Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")

_cache = {}


def _font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(text, size, weight=400, mono=False, tracking=0.0):
    """Advance width of `text` in user units."""
    path = MNO if mono else (BLD if weight >= 600 else REG)
    w = _font(path, size).getlength(text)
    return w + tracking * max(0, len(text) - 1)


WARN = []


def wrap(text, max_w, size, weight=400, mono=False):
    """Greedy word wrap to `max_w` user units."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if cur and tw(trial, size, weight, mono) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    for ln in lines:
        if tw(ln, size, weight, mono) > max_w:
            WARN.append(f"unbreakable {ln!r} {tw(ln, size, weight, mono):.0f} > {max_w:.0f}")
    return lines


def shrink(text, max_w, size, weight=400, mono=False, floor=15):
    """Largest size <= `size` at which `text` fits `max_w`."""
    while size > floor and tw(text, size, weight, mono) > max_w:
        size -= 1
    if tw(text, size, weight, mono) > max_w:
        WARN.append(f"overflow {text!r} at {size}px: {tw(text, size, weight, mono):.0f} > {max_w:.0f}")
    return size


# ---------------------------------------------------------------- palette
INK = "#1f2430"
MUTED = "#64718a"
FAINT = "#94a3b8"
PAGE = "#f8fafc"
CARD = "#ffffff"
EDGE = "#dbe3ef"
ARROW = "#7d8ba3"

C = {
    "token":  dict(stroke="#3381db", fill="#e8f1fc", text="#1a4d8f"),
    "pos":    dict(stroke="#d08a1e", fill="#fdf2dd", text="#8a5905"),
    "qk":     dict(stroke="#7a5ad0", fill="#efe9fd", text="#4b3193"),
    "v":      dict(stroke="#109188", fill="#ddf2f0", text="#0a5f59"),
    "out":    dict(stroke="#2f9e68", fill="#e7f6ee", text="#1a6b45"),
    "ghost":  dict(stroke="#b6c1d2", fill="#f4f7fb", text="#8d9ab0"),
    "plain":  dict(stroke="#c8d3e2", fill="#fbfcfe", text=INK),
}


class Svg:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = []

    def add(self, s):
        self.parts.append("  " + s)
        return self

    # -- primitives ------------------------------------------------
    def rect(self, x, y, w, h, r=16, fill="none", stroke="none", sw=3, dash=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        return self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" '
                        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"{d}{o}/>')

    def text(self, x, y, s, size=24, weight=400, fill=INK, anchor="start",
             mono=False, tracking=0.0, opacity=None):
        fam = "DejaVu Sans Mono, monospace" if mono else "Noto Sans, sans-serif"
        t = f' letter-spacing="{tracking:g}"' if tracking else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        return self.add(f'<text x="{x:g}" y="{y:g}" font-family="{fam}" font-size="{size:g}" '
                        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{t}{o}>'
                        f'{escape(s)}</text>')

    def path(self, d, stroke=ARROW, sw=3.5, marker=None, dash=None, fill="none", cap="round"):
        m = f' marker-end="url(#{marker})"' if marker else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}" '
                        f'stroke-linecap="{cap}" stroke-linejoin="round"{m}{da}/>')

    def circle(self, cx, cy, r, fill="none", stroke="none", sw=3):
        return self.add(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{fill}" '
                        f'stroke="{stroke}" stroke-width="{sw:g}"/>')

    # -- composites ------------------------------------------------
    def node(self, x, y, w, h, label, sub=None, kind="plain", label_size=25,
             sub_size=20, mono=False, dash=None, r=16, opacity=None, sub_fill=None):
        """A rounded box with a bold label and an optional muted sub-label."""
        c = C[kind]
        self.rect(x, y, w, h, r=r, fill=c["fill"], stroke=c["stroke"], dash=dash, opacity=opacity)
        cx, avail = x + w / 2, w - 24
        label_size = shrink(label, avail, label_size, 700, mono)
        if sub:
            sub_size = shrink(sub, avail, sub_size, 400)
            self.text(cx, y + h / 2 - 4, label, label_size, 700, c["text"], "middle", mono=mono, opacity=opacity)
            self.text(cx, y + h / 2 + sub_size + 3, sub, sub_size, 400, sub_fill or MUTED,
                      "middle", opacity=opacity)
        else:
            self.text(cx, y + h / 2 + label_size * 0.35, label, label_size, 700, c["text"], "middle",
                      mono=mono, opacity=opacity)
        return self

    def plus(self, cx, cy, r=25, color=ARROW, opacity=None):
        """A vector '+ in a circle' so we never depend on math glyph coverage."""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        self.add(f'<g{o}><circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="#ffffff" stroke="{color}" '
                 f'stroke-width="3"/>'
                 f'<path d="M{cx - r * 0.5:g} {cy:g} H{cx + r * 0.5:g} M{cx:g} {cy - r * 0.5:g} '
                 f'V{cy + r * 0.5:g}" stroke="{color}" stroke-width="3.5" '
                 f'stroke-linecap="round"/></g>')
        return self

    def wrapped(self, x, y, text, max_w, size=22, fill=MUTED, weight=400, lh=29, anchor="start"):
        for i, ln in enumerate(wrap(text, max_w, size, weight)):
            self.text(x, y + i * lh, ln, size, weight, fill, anchor)
        return self

    def render(self):
        markers = []
        for name, col in [("aGrey", ARROW), ("aGreen", "#2f9e68"), ("aAmber", "#d08a1e"),
                          ("aPurple", "#7a5ad0"), ("aTeal", "#109188"), ("aFaint", "#b6c1d2")]:
            markers.append(
                f'<marker id="{name}" markerUnits="userSpaceOnUse" markerWidth="15" '
                f'markerHeight="14" refX="14" refY="7" orient="auto">'
                f'<path d="M0,0.5 L14,7 L0,13.5 Z" fill="{col}"/></marker>')
        body = "\n".join(self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">\n'
                f'  <defs>\n    ' + "\n    ".join(markers) + '\n  </defs>\n'
                f'  <rect width="{self.w}" height="{self.h}" fill="#ffffff"/>\n'
                f'{body}\n</svg>\n')

    def save(self, path):
        open(path, "w").write(self.render())
        print("wrote", path)
        for w in WARN:
            print("  !!", w)
        WARN.clear()
