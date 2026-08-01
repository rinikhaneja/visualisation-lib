"""Supporting panels for the US carbon story.

Renders two standalone figures (reusing existing viz_lib functions):

1. us_ghg_percapita.png  — US per-capita greenhouse-gas trend (split_panel_line)
2. us_cumulative_share.png — US share of global cumulative CO2 by fuel (ranked_bar)
"""

from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from viz_lib import ranked_bar, load_dataset  # noqa: E402
from viz_lib.theme import apply_theme, series_color  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "figures"
LATEST = 2024


def ghg_panel() -> None:
    apply_theme()
    df = load_dataset("us_percapita_ghg")
    col = [c for c in df.columns if "greenhouse" in c.lower()][0]
    x, y = df["Year"].to_numpy(), df[col].to_numpy()

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    color = series_color(0)
    ax.plot(x, y, color=color, linewidth=2.2, solid_capstyle="round")
    ax.fill_between(x, y, color=color, alpha=0.08)
    ax.set_ylim(0, y.max() * 1.08)
    ax.set_xlim(x.min(), x.max())

    # direct end label + a 2024 tick, OWID-style
    ax.annotate(f"{y[-1]:.0f} t", xy=(x[-1], y[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", ha="left",
                fontsize=11, fontweight="bold", color=color, annotation_clip=False)
    ticks = [t for t in ax.get_xticks() if x.min() <= t <= x.max()]
    if not ticks or x.max() - ticks[-1] > 6:
        ticks.append(x.max())
    else:
        ticks[-1] = x.max()  # snap a too-close tick onto 2024
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(int(t)) for t in ticks])

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    ax.set_ylabel("Tonnes CO₂-equivalent per person", color="#52514e")
    ax.set_title("Even as CO₂ fell, the US still emits ~18 t per person a year",
                 loc="left", fontsize=14, fontweight="bold", pad=20)
    ax.annotate("Per-capita greenhouse gases (CO₂ + methane + N₂O), incl. land use, 1850–2024",
                xy=(0, 1.0), xycoords="axes fraction", xytext=(0, 6),
                textcoords="offset points", ha="left", va="bottom",
                fontsize=10.5, color="#52514e")
    fig.tight_layout()
    fig.savefig(OUT / "us_ghg_percapita.png", dpi=150, bbox_inches="tight")
    print("wrote", OUT / "us_ghg_percapita.png")


def share_panel() -> None:
    names = {"Oil": "share_cumulative_oil",
             "Coal": "share_cumulative_coal",
             "Cement": "share_cumulative_cement"}
    rows = []
    for fuel, name in names.items():
        d = load_dataset(name)
        col = [c for c in d.columns if "Share" in c][0]
        val = d[(d["Entity"] == "United States") & (d["Year"] == LATEST)][col].iloc[0]
        rows.append({"Fuel": fuel, "share": val})
    df = pd.DataFrame(rows)

    fig = ranked_bar(
        df, category="Fuel", value="share", value_fmt="{:.0f}%",
        title="The US alone caused a quarter of all CO₂ ever emitted from oil",
        subtitle="US share of the world's cumulative CO₂ emissions, by source (1750–2024)",
        note="Source: Global Carbon Budget (2025) via Our World in Data.",
    )
    fig.savefig(OUT / "us_cumulative_share.png", dpi=150, bbox_inches="tight")
    print("wrote", OUT / "us_cumulative_share.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ghg_panel()
    share_panel()


if __name__ == "__main__":
    main()
