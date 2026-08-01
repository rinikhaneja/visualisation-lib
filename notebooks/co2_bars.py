"""Two CO2-per-capita bar charts, built with viz_lib."""
from pathlib import Path
import sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from viz_lib import ranked_bar, load_dataset  # noqa: E402
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "figures"
VALUE = "CO₂ emissions per capita"
LATEST, PRIOR = 2024, 2014
OIL = ["Qatar", "Kuwait", "Brunei", "Bahrain", "Trinidad and Tobago",
       "Saudi Arabia", "United Arab Emirates", "Oman"]
ECON = ["United States", "Russia", "North America", "China",
        "European Union (27)", "World", "United Kingdom", "India"]

def load_wide() -> pd.DataFrame:
    """Return one row per entity with the LATEST and PRIOR year as columns."""
    df = load_dataset("co2_per_capita")
    df = df[df["Year"].isin([LATEST, PRIOR])]
    wide = df.pivot_table(index="Entity", columns="Year", values=VALUE)
    wide.columns = [f"y{c}" for c in wide.columns]
    return wide.reset_index()

def subset(wide: pd.DataFrame, names: list[str]) -> pd.DataFrame:
    return wide[wide["Entity"].isin(names)].copy()

def main() -> None:
    wide = load_wide()
    OUT.mkdir(parents=True, exist_ok=True)
    # shared color scale so a shade means the same emissions in both charts
    plotted = subset(wide, OIL + ECON)
    vmax = plotted[f"y{LATEST}"].max()
    fig1 = ranked_bar(
        subset(wide, OIL), category="Entity", value=f"y{LATEST}",
        vmax=vmax, unit="t",
        title="A few small, oil-rich nations emit the most CO₂ per person",
    )
    fig1.savefig(OUT / "co2_oil_producers.png", dpi=150, bbox_inches="tight")
    fig2 = ranked_bar(
        subset(wide, ECON), category="Entity", value=f"y{LATEST}",
        vmax=vmax, unit="t",
        title="Among big economies, the US still emits the most per person",
        subtitle="Tonnes of CO₂ per person, 2024 — shaded on the same scale as oil producers",
    )
    fig2.savefig(OUT / "co2_major_economies.png", dpi=150, bbox_inches="tight")
    print("wrote", OUT / "co2_oil_producers.png")
    print("wrote", OUT / "co2_major_economies.png")

if __name__ == "__main__":
    main()
