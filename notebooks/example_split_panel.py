"""Example: split-panel line plot of CO2 emissions per capita.

Run from the project root::

    python notebooks/example_split_panel.py

Writes the figure to ``reports/figures/co2_split_panel.png``.

The data here is illustrative (values are in the real tonnes-per-capita range
but are not exact) — it exists to demonstrate the plot, not to cite figures.
"""

from pathlib import Path
import sys

# Make ``src`` importable when running this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from viz_lib import split_panel_line  # noqa: E402

YEARS = [1960, 1970, 1980, 1990, 2000, 2010, 2020]

SERIES = {
    "Qatar": [60, 52, 42, 28, 55, 42, 35],
    "Trinidad & Tobago": [8, 12, 18, 14, 20, 32, 26],
    "Kuwait": [55, 45, 22, 20, 28, 30, 25],
    "UAE": [None, 45, 38, 30, 32, 25, 20],
    "United States": [16, 21, 20, 19.5, 20.5, 17.5, 14],
    "China": [1, 1, 1.5, 2, 2.7, 6.5, 8],
    "Russia": [10, 13, 15, 15, 10, 11, 11],
    "United Kingdom": [11, 11.5, 10.5, 10, 9, 7.5, 5],
    "India": [0.3, 0.4, 0.5, 0.7, 1, 1.4, 1.8],
    "World": [3, 3.8, 4.2, 4, 4, 4.7, 4.5],
}

PANELS = {
    "A · Oil exporters & microstates": ["Qatar", "Trinidad & Tobago", "Kuwait", "UAE"],
    "B · Major economies & baselines": [
        "United States", "China", "Russia", "United Kingdom", "India", "World",
    ],
}


def main() -> None:
    fig = split_panel_line(
        YEARS,
        SERIES,
        PANELS,
        x_label="Year",
        y_label="Tonnes CO₂ per capita",
        suptitle="CO₂ per capita — split panels",
    )
    out = Path(__file__).resolve().parents[1] / "reports" / "figures" / "co2_split_panel.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
