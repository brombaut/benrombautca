"""Regenerate every blog diagram (SVG + PNG). Run: python3 scripts/diagrams/build.py"""
import pathlib
import runpy
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

for script in sorted(HERE.glob("d_*.py")):
    print(script.name)
    runpy.run_path(str(script), run_name="__main__")
