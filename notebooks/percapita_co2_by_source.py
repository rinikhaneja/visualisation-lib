"""Replica of the Our World in Data chart
"Per capita CO2 emissions by source, 2024", built with viz_lib.stacked_bar.

Reads the bundled ``percapita_co2_by_source`` dataset and writes
``reports/figures/percapita_co2_by_source.png``.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from viz_lib import stacked_bar, load_dataset  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "reports" / "figures" / "percapita_co2_by_source.png"

# left-to-right stack + legend order, matching OWID
SEGMENTS = ["Coal", "Oil", "Gas", "Flaring", "Cement", "Other industry"]

# OWID's source palette (override our default so the replica matches)
OWID_COLORS = {
    "Coal": "#6d6e70",
    "Oil": "#c14b62",
    "Gas": "#8c6bb1",
    "Flaring": "#c8a45c",
    "Cement": "#2f8e7f",
    "Other industry": "#6d8fc5",
}


def owid_tonnes(v: float) -> str:
    """OWID number style: one decimal below 10 t, whole tonnes at/above 10 t."""
    return f"{v:.0f} t" if v >= 10 else f"{v:.1f} t"


def main() -> None:
    df = load_dataset("percapita_co2_by_source")

    fig = stacked_bar(
        df, category="Entity", segments=SEGMENTS,
        colors=OWID_COLORS,
        value_fmt=owid_tonnes,      # adaptive "6.4 t" / "34 t"
        seg_label_min=0.05,         # label segments down to ~2 t (as OWID does)
        title="Per capita CO₂ emissions by source, 2024",
        note="Data source: Global Carbon Budget (2025); Population based on various "
             "sources (2024).  OurWorldinData.org/co2-and-greenhouse-gas-emissions | CC BY",
        figsize=(12, 9),
    )
    # thin baseline axis at x=0, like the OWID chart
    ax = fig.axes[0]
    ax.axvline(0, color="#c3c2b7", linewidth=1.0, zorder=2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="#fcfcfb")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
