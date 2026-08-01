"""Hero chart: US CO2 emissions by fuel or industry, 1800-2024."""
from pathlib import Path
import sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from viz_lib import stacked_area, load_dataset  # noqa: E402
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "figures" / "us_co2_hero.png"
# bottom-to-top stacking order (coal is the historical base)
FUELS = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other industry"]

def main() -> None:
    df = load_dataset("us_co2_by_fuel")
    # tonnes -> billion tonnes for readable labels
    for f in FUELS:
        df[f] = pd.to_numeric(df[f], errors="coerce") / 1e9
    fig = stacked_area(
        df, x="Year", series=FUELS,
        y_label="Billion tonnes CO₂ per year",
        title="A century of American carbon: coal gave way to oil and gas",
        subtitle="US CO₂ emissions by fuel or industry, 1800–2024 (billion tonnes per year)",
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight")
    print("wrote", OUT)

if __name__ == "__main__":
    main()
