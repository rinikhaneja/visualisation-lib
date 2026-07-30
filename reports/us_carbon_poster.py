"""Assemble the US carbon-story poster from viz_lib panels.

Composes the hero + two supporting panels + title/intro/footer onto one
print-ready canvas using matplotlib GridSpec. Each panel calls a viz_lib
function with a passed-in Axes, so there is no new plotting logic here — only
layout and the editorial text frame.

Run from the project root::

    python reports/us_carbon_poster.py
"""

from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from viz_lib import stacked_area, ranked_bar, load_dataset  # noqa: E402
from viz_lib.theme import apply_theme, series_color  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "figures" / "us_carbon_poster.png"
LATEST = 2024
FUELS = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other industry"]
EVENTS = [
    {"year": 1932, "label": "1932\nGreat Depression", "y": 0.42},
    {"year": 1945, "label": "1945\nWWII", "y": 0.72},
    {"year": 1973, "label": "1973\nOil shock", "y": 0.9},
    {"year": 2007, "label": "2007\nemissions peak", "y": 0.98},
    {"year": 2020, "label": "2020\nCOVID", "y": 0.62},
]
INTRO = (
    "For two centuries the United States built its economy on fossil fuels. "
    "Coal powered the first industrial century; oil and gas took over after "
    "1945. Emissions peaked in 2007 and have fallen since — yet the US still "
    "emits far above the world average and remains the largest single "
    "contributor to the CO₂ humanity has ever released."
)
FOOTER = "Source: Global Carbon Budget (2025) via Our World in Data (CC BY).  Built with viz_lib."


def draw_ghg(ax) -> None:
    df = load_dataset("us_percapita_ghg")
    col = [c for c in df.columns if "greenhouse" in c.lower()][0]
    x, y = df["Year"].to_numpy(), df[col].to_numpy()
    color = series_color(0)
    ax.plot(x, y, color=color, linewidth=2.2, solid_capstyle="round")
    ax.fill_between(x, y, color=color, alpha=0.08)
    ax.set_ylim(0, y.max() * 1.08)
    ax.set_xlim(x.min(), x.max())
    ax.annotate(f"{y[-1]:.0f} t", xy=(x[-1], y[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", ha="left",
                fontsize=11, fontweight="bold", color=color, annotation_clip=False)
    ticks = [t for t in ax.get_xticks() if x.min() <= t <= x.max()]
    if not ticks or x.max() - ticks[-1] > 6:
        ticks.append(x.max())
    else:
        ticks[-1] = x.max()
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(int(t)) for t in ticks])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Even as CO₂ fell, the US still emits ~18 t per person",
                 loc="left", fontsize=13, fontweight="bold", pad=16)
    ax.annotate("Per-capita greenhouse gases (CO₂ + CH₄ + N₂O), 1850–2024",
                xy=(0, 1.0), xycoords="axes fraction", xytext=(0, 4),
                textcoords="offset points", ha="left", va="bottom",
                fontsize=9.5, color="#52514e")


def load_hero() -> pd.DataFrame:
    df = load_dataset("us_co2_by_fuel")
    for f in FUELS:
        df[f] = pd.to_numeric(df[f], errors="coerce") / 1e9
    return df


def load_share() -> pd.DataFrame:
    names = {"Oil": "share_cumulative_oil", "Coal": "share_cumulative_coal",
             "Cement": "share_cumulative_cement"}
    rows = []
    for fuel, name in names.items():
        d = load_dataset(name)
        col = [c for c in d.columns if "Share" in c][0]
        val = d[(d["Entity"] == "United States") & (d["Year"] == LATEST)][col].iloc[0]
        rows.append({"Fuel": fuel, "share": val})
    return pd.DataFrame(rows)


def build_poster():
    """Build and return the poster Figure from the bundled datasets."""
    apply_theme()
    fig = plt.figure(figsize=(12, 15))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.45, 1.0],
                          top=0.78, bottom=0.06, left=0.08, right=0.95,
                          hspace=0.42, wspace=0.28)

    # editorial frame
    fig.text(0.08, 0.965, "A CENTURY OF AMERICAN CARBON", fontsize=30,
             fontweight="bold", ha="left", va="top", color="#0b0b0b")
    fig.text(0.08, 0.925, INTRO, fontsize=12.5, ha="left", va="top",
             color="#52514e", wrap=True)
    fig.text(0.08, 0.025, FOOTER, fontsize=9, ha="left", va="bottom", color="#898781")

    # hero (spans the top row)
    ax_hero = fig.add_subplot(gs[0, :])
    stacked_area(load_hero(), x="Year", series=FUELS, ax=ax_hero,
                 y_label="Billion tonnes CO₂ / year",
                 title="Coal gave way to oil and gas",
                 subtitle="US CO₂ emissions by fuel or industry, 1800–2024",
                 events=EVENTS)

    # supporting panels
    draw_ghg(fig.add_subplot(gs[1, 0]))
    ranked_bar(load_share(), category="Fuel", value="share", value_fmt="{:.0f}%",
               ax=fig.add_subplot(gs[1, 1]),
               title="A quarter of all oil CO₂ ever, from one country",
               subtitle="US share of the world's cumulative CO₂, by source")
    return fig


def main() -> None:
    fig = build_poster()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="#fcfcfb")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
