"""Shared visual identity for every plot in the library."""
from __future__ import annotations
import matplotlib as mpl
#: Sequential "smog / heat" ramp for CO2 magnitude: pale haze -> deep ember.
#: Lightness decreases monotonically, so it stays legible in black & white and
#: for colorblind readers (darker always means more emissions).
SMOG: list[str] = ["#f4d06a", "#eaa23b", "#df6b2e", "#c0392b", "#7b1f16"]

def smog_color(value: float, vmax: float) -> tuple:
    """Map ``value`` (0..``vmax``) onto the SMOG ramp; returns an RGBA tuple."""
    import matplotlib.colors as mcolors
    cmap = mcolors.LinearSegmentedColormap.from_list("smog", SMOG)
    frac = 0.0 if vmax <= 0 else max(0.0, min(1.0, value / vmax))
    # start a little into the ramp so the smallest bars aren't near-white
    return cmap(0.12 + 0.88 * frac)

#: Categorical palette, light surface, in fixed assignment order.
PALETTE: list[str] = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]
# Chrome / ink for the light surface these plots render on.
_INK_PRIMARY = "#0b0b0b"
_INK_SECONDARY = "#52514e"
_MUTED = "#898781"
_GRID = "#e1e0d9"
_AXIS = "#c3c2b7"
_SURFACE = "#fcfcfb"
_FONT_STACK = ["system-ui", "Segoe UI", "DejaVu Sans", "Arial", "sans-serif"]

def series_color(index: int) -> str:
    """Return the palette hue for the *index*-th series (0-based)."""
    if index < 0 or index >= len(PALETTE):
        raise IndexError(
            f"series index {index} out of range; the categorical palette has "
            f"{len(PALETTE)} slots. Fold extra series into 'Other' or facet."
        )
    return PALETTE[index]

def apply_theme() -> None:
    """Apply the library's rcParams globally."""
    mpl.rcParams.update(
        {
            "figure.facecolor": _SURFACE,
            "axes.facecolor": _SURFACE,
            "savefig.facecolor": _SURFACE,
            "font.family": "sans-serif",
            "font.sans-serif": _FONT_STACK,
            "font.size": 11,
            "text.color": _INK_PRIMARY,
            "axes.edgecolor": _AXIS,
            "axes.labelcolor": _INK_SECONDARY,
            "axes.titlecolor": _INK_PRIMARY,
            "axes.titlesize": 12.5,
            "axes.titleweight": "bold",
            "axes.linewidth": 1.0,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": _GRID,
            "grid.linewidth": 1.0,
            "xtick.color": _MUTED,
            "ytick.color": _MUTED,
            "xtick.labelsize": 10.5,
            "ytick.labelsize": 10.5,
            "axes.prop_cycle": mpl.cycler(color=PALETTE),
            "legend.frameon": False,
            "legend.fontsize": 10.5,
        }
    )
