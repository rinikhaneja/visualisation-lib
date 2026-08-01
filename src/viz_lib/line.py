"""Line plots, including the split-panel variant for mixed-scale series."""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np
import matplotlib.pyplot as plt

from .theme import apply_theme, series_color

# Types kept loose on purpose so the function works with plain lists/dicts and
# with pandas Series/DataFrame columns alike, with no hard pandas dependency.
Numeric = Sequence[float]
SeriesData = Mapping[str, Numeric]
PanelSpec = Mapping[str, Sequence[str]] | Sequence[Mapping]


def _clean(y: Numeric) -> np.ndarray:
    """Coerce a y-sequence to float ndarray, turning None into NaN (a gap)."""
    return np.array([np.nan if v is None else float(v) for v in y], dtype=float)


def _normalize_panels(panels: PanelSpec) -> list[tuple[str, list[str]]]:
    """Return an ordered list of ``(title, [series_names])``."""
    if isinstance(panels, Mapping):
        return [(title, list(names)) for title, names in panels.items()]
    out = []
    for spec in panels:
        out.append((spec.get("title", ""), list(spec["series"])))
    return out


def split_panel_line(
    x: Numeric,
    series: SeriesData,
    panels: PanelSpec,
    *,
    orientation: str = "horizontal",
    x_label: str | None = None,
    y_label: str | None = None,
    suptitle: str | None = None,
    direct_labels: bool = True,
    sharey: bool = False,
    colors=None,
    figsize: tuple[float, float] | None = None,
    ax=None,
):
    """Draw one metric across several series, split into panels."""
    apply_theme()
    panel_list = _normalize_panels(panels)
    n = len(panel_list)
    if n == 0:
        raise ValueError("panels is empty — nothing to draw")
    overrides = dict(colors) if isinstance(colors, Mapping) else {}
    x_arr = np.asarray(x, dtype=float)
    # --- axes ---------------------------------------------------------------
    owns_fig = ax is None
    if ax is not None:
        axes = np.atleast_1d(ax).ravel()
        if len(axes) != n:
            raise ValueError(f"ax has {len(axes)} axes but there are {n} panels")
        fig = axes[0].figure
    else:
        if figsize is None:
            figsize = (5.0 * n, 3.6) if orientation == "horizontal" else (6.4, 3.0 * n)
        if orientation == "horizontal":
            fig, axes = plt.subplots(1, n, figsize=figsize, sharey=sharey)
        elif orientation == "vertical":
            fig, axes = plt.subplots(n, 1, figsize=figsize, sharex=True, sharey=sharey)
        else:
            raise ValueError("orientation must be 'horizontal' or 'vertical'")
        axes = np.atleast_1d(axes).ravel()
    # --- draw each panel ----------------------------------------------------
    for pi, (ax_i, (title, names)) in enumerate(zip(axes, panel_list)):
        end_labels = []  # (y_value, x_value, name, color) for de-collision
        for si, name in enumerate(names):
            if name not in series:
                raise KeyError(f"panel '{title}' references unknown series '{name}'")
            y = _clean(series[name])
            if y.shape != x_arr.shape:
                raise ValueError(
                    f"series '{name}' has {y.shape[0]} points but x has "
                    f"{x_arr.shape[0]}"
                )
            color = overrides.get(name, series_color(si))
            ax_i.plot(
                x_arr, y, color=color, linewidth=2.0,
                solid_joinstyle="round", solid_capstyle="round", label=name,
            )
            if direct_labels:
                valid = np.where(~np.isnan(y))[0]
                if valid.size:
                    i = valid[-1]
                    end_labels.append((float(y[i]), float(x_arr[i]), name, color))
        if title:
            ax_i.set_title(title, loc="left", pad=8)
        if x_label:
            ax_i.set_xlabel(x_label)
        # y label only on the leading panel to avoid repetition
        if y_label and pi == 0:
            ax_i.set_ylabel(y_label)
        ax_i.margins(y=0.08)
        if direct_labels:
            # leave head-room on the right for the end labels
            ax_i.margins(x=0.04)
            _pad_right(ax_i, x_arr)
            _place_end_labels(ax_i, end_labels)
        else:
            ax_i.legend(loc="best")
    if suptitle:
        fig.suptitle(suptitle, x=0.02, ha="left", fontsize=14, fontweight="bold")
    if owns_fig:
        fig.tight_layout()
    return fig


def _place_end_labels(ax, labels):
    """Draw right-end series labels, nudged apart so they never overlap."""
    if not labels:
        return
    lo, hi = ax.get_ylim()
    # one label row ~ 6% of the visible y-range; keep them inside the axes
    gap = (hi - lo) * 0.06
    labels = sorted(labels, key=lambda t: t[0])
    prev = None
    for y_val, x_val, name, color in labels:
        y_text = y_val if prev is None else max(y_val, prev + gap)
        prev = y_text
        ax.annotate(
            name,
            xy=(x_val, y_text),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            fontsize=10.5,
            fontweight="bold",
            color=color,
            annotation_clip=False,
        )


def _pad_right(ax, x_arr):
    """Widen the x-limit so right-hand direct labels don't clip."""
    lo, hi = float(np.nanmin(x_arr)), float(np.nanmax(x_arr))
    span = hi - lo or 1.0
    ax.set_xlim(lo - span * 0.02, hi + span * 0.18)
