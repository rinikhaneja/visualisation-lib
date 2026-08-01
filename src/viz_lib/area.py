"""Stacked area chart — composition (part-to-whole) over time."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from .theme import apply_theme, series_color
_MUTED = "#898781"
_SECOND = "#52514e"
_SURFACE = "#fcfcfb"

def stacked_area(
    df,
    x: str,
    series: list[str],
    *,
    colors=None,
    y_label: str | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    note: str | None = None,
    direct_labels: bool = True,
    ax=None,
    figsize: tuple[float, float] | None = None,
):
    """Draw a stacked area chart from a pandas DataFrame."""
    apply_theme()
    data = df.sort_values(x)
    xv = data[x].to_numpy(dtype=float)
    stacks = [np.nan_to_num(data[s].to_numpy(dtype=float), nan=0.0) for s in series]
    overrides = dict(colors) if isinstance(colors, dict) else {}
    cols = [overrides.get(s, series_color(i)) for i, s in enumerate(series)]
    owns_fig = ax is None
    if owns_fig:
        fig, ax = plt.subplots(figsize=figsize or (11, 6))
    else:
        fig = ax.figure
    # 2px surface gap between bands (checklist: separate the fills)
    ax.stackplot(xv, *stacks, colors=cols, edgecolor=_SURFACE, linewidth=0.8)
    ax.set_xlim(xv.min(), xv.max())
    top = np.sum(stacks, axis=0).max()
    ax.set_ylim(0, top * 1.02)
    # always mark the final year (e.g. 2024) as a tick, like the OWID charts
    ticks = [t for t in ax.get_xticks() if xv.min() <= t <= xv.max()]
    if not ticks or xv.max() - ticks[-1] > 6:
        ticks.append(xv.max())
    else:
        ticks[-1] = xv.max()  # snap a too-close tick onto the exact end
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{int(t)}" for t in ticks])
    # direct band labels at the right end, nudged apart if they collide
    if direct_labels:
        cum = np.cumsum(stacks, axis=0)
        centers = []
        for i, s in enumerate(series):
            bottom = cum[i - 1][-1] if i else 0.0
            centers.append(((bottom + cum[i][-1]) / 2, s, cols[i]))
        _labels_at_right(ax, xv.max(), centers, top)
    # chrome: mute everything that isn't data (checklist: mute the lines)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(_MUTED)
    ax.spines["bottom"].set_color(_MUTED)
    ax.tick_params(length=0)
    ax.grid(False)
    if y_label:
        ax.set_ylabel(y_label, color=_SECOND)
    if title:
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold", pad=26)
    if subtitle:
        ax.annotate(subtitle, xy=(0, 1.0), xycoords="axes fraction",
                    xytext=(0, 8), textcoords="offset points", ha="left",
                    va="bottom", fontsize=11.5, color=_SECOND)
    if note:
        ax.annotate(note, xy=(0, 0), xycoords="axes fraction", xytext=(0, -34),
                    textcoords="offset points", ha="left", va="top",
                    fontsize=8.5, color=_MUTED)
    if owns_fig:
        fig.tight_layout()
    return fig

def _labels_at_right(ax, x_end, centers, top):
    """Place band labels at the right edge, spread so they don't overlap."""
    gap = top * 0.045
    centers = sorted(centers, key=lambda t: t[0])
    prev = None
    for y_val, name, color in centers:
        y_text = y_val if prev is None else max(y_val, prev + gap)
        prev = y_text
        ax.annotate(name, xy=(x_end, y_text), xytext=(8, 0),
                    textcoords="offset points", va="center", ha="left",
                    fontsize=10.5, fontweight="bold", color=color,
                    annotation_clip=False)
