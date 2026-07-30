"""Hero chart: US CO2 emissions by fuel or industry, 1800-2024.

The centerpiece of the US carbon-story poster — a stacked area of absolute
emissions with dated event annotations. Reads ``data/raw/us_co2_by_fuel.csv``
and writes ``reports/figures/us_co2_hero.png``.
"""

from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from viz_lib import stacked_area  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "us_co2_by_fuel.csv"
OUT = ROOT / "reports" / "figures" / "us_co2_hero.png"

# bottom-to-top stacking order (coal is the historical base)
FUELS = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other industry"]

EVENTS = [
    {"year": 1918, "label": "1918\nWWI peak", "y": 0.55},
    {"year": 1932, "label": "1932\nGreat Depression", "y": 0.42},
    {"year": 1945, "label": "1945\nWWII", "y": 0.72},
    {"year": 1973, "label": "1973\nOil shock", "y": 0.9},
    {"year": 2007, "label": "2007\nemissions peak", "y": 0.98},
    {"year": 2020, "label": "2020\nCOVID", "y": 0.62},
]


def main() -> None:
    df = pd.read_csv(CSV)
    # tonnes -> billion tonnes for readable labels
    for f in FUELS:
        df[f] = pd.to_numeric(df[f], errors="coerce") / 1e9

    fig = stacked_area(
        df, x="Year", series=FUELS,
        y_label="Billion tonnes CO₂ per year",
        title="A century of American carbon: coal gave way to oil and gas",
        subtitle="US CO₂ emissions by fuel or industry, 1800–2024 (billion tonnes per year)",
        note="Source: Global Carbon Budget (2025) via Our World in Data.",
        events=EVENTS,
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
