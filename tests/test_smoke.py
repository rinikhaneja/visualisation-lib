"""Smoke tests: the example scripts in notebooks/ run end-to-end and emit PNGs."""
import importlib.util
import matplotlib
matplotlib.use("Agg")  # headless: the scripts render without a display
import pytest
from pathlib import Path

NOTEBOOKS = Path(__file__).resolve().parents[1] / "notebooks"

def _load(script):
    """Import a notebooks/*.py script as a module by file path."""
    path = NOTEBOOKS / script
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

@pytest.mark.parametrize("script,outputs", [
    ("co2_bars.py", ["co2_oil_producers.png", "co2_major_economies.png"]),
    ("us_co2_hero.py", ["us_co2_hero.png"]),
])
def test_script_renders_figures(script, outputs):
    """Running a script's main() writes its expected PNG(s) to reports/figures."""
    mod = _load(script)
    mod.main()
    figures = NOTEBOOKS.parent / "reports" / "figures"
    for name in outputs:
        assert (figures / name).exists(), f"{script} did not write {name}"
