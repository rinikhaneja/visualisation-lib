"""Shared visual identity for every plot in the library."""
from __future__ import annotations
import matplotlib as mpl
#: Sequential "smog / heat" ramp for CO2 magnitude: pale haze -> deep ember.
SMOG: list[str] = ["#f4d06a", "#eaa23b", "#df6b2e", "#c0392b", "#7b1f16"]

def smog_color(value: float, vmax: float) -> tuple:
    """Map value (0..vmax) onto the SMOG ramp; returns an RGBA tuple."""
    import matplotlib.colors as mcolors
    cmap = mcolors.LinearSegmentedColormap.from_list("smog", SMOG)
    frac = 0.0 if vmax <= 0 else max(0.0, min(1.0, value / vmax))
    return cmap(0.12 + 0.88 * frac)

#: Categorical palette (blue, orange, aqua, yellow, magenta, green, violet, red).
PALETTE: list[str] = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
                      "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
_SURFACE = "#fcfcfb"
_FONT_STACK = ["system-ui", "Segoe UI", "DejaVu Sans", "Arial", "sans-serif"]

def series_color(index: int) -> str:
    """Return the palette hue for the index-th series (cycles past 8)."""
    return PALETTE[index % len(PALETTE)]

def apply_theme() -> None:
    """Apply the library's rcParams globally."""
    mpl.rcParams.update({
        "figure.facecolor": _SURFACE,
        "axes.facecolor": _SURFACE,
        "savefig.facecolor": _SURFACE,
        "font.family": "sans-serif",
        "font.sans-serif": _FONT_STACK,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "legend.frameon": False,
    })
