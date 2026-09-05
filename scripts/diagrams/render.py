"""Rasterize an SVG to PNG with librsvg (via GdkPixbuf), the renderer the blog images use."""
import re
import sys
import gi

gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf  # noqa: E402

SCALE = 1.5      # source units are sized for ~800px display; 1.5x keeps it crisp on retina


def render_png(svg_path, scale=SCALE):
    svg_path = str(svg_path)
    src = open(svg_path).read()
    w = float(re.search(r'width="([\d.]+)"', src).group(1))
    h = float(re.search(r'height="([\d.]+)"', src).group(1))
    png_path = svg_path[:-4] + ".png"
    pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(svg_path, int(w * scale), int(h * scale), True)
    pb.savev(png_path, "png", [], [])
    print(f"  -> {png_path}  {pb.get_width()}x{pb.get_height()}")
    return png_path


if __name__ == "__main__":
    for p in sys.argv[1:]:
        render_png(p)
