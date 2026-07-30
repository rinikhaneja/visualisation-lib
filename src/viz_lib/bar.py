"""Ranked horizontal bar chart, built to the Evergreen Data Viz Checklist.

One job: take a tidy pandas DataFrame and draw a sorted, directly-labelled
horizontal bar chart that a non-technical reader understands at a glance.

Checklist choices baked in: bars sorted by value (not alphabetically), a zero
baseline, direct value labels, no gridlines / border / redundant axis, a
takeaway title, and a CO2-themed sequential color ramp that stays legible in
black & white and for colorblind readers.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

from .theme import apply_theme, smog_color, series_color

_UP, _DOWN = "▲", "▼"  # ▲ ▼
_SURFACE = "#fcfcfb"


def _readable_ink(color) -> str:
    """Pick black or white text for a filled segment by its luminance."""
    r, g, b = mcolors.to_rgb(color)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return "#0b0b0b" if lum > 0.6 else "#ffffff"


def ranked_bar(
    df,
    category: str,
    value: str,
    *,
    compare: str | None = None,
    reference: float | None = None,
    reference_label: str | None = None,
    vmax: float | None = None,
    unit: str = "",
    value_fmt: str = "{:.1f}",
    title: str | None = None,
    subtitle: str | None = None,
    note: str | None = None,
    ascending: bool = False,
    ax=None,
    figsize: tuple[float, float] | None = None,
):
    """Draw a sorted horizontal bar chart from a pandas DataFrame.

    Parameters
    ----------
    df
        A pandas DataFrame (MVP input — DataFrames only).
    category, value
        Column names: the label per bar and the numeric length to rank by.
    compare
        Optional column with an earlier value; when given, each bar gets a
        muted ``▲ / ▼ %`` tag showing the change to ``value`` (the story of
        who rose or fell).
    reference, reference_label
        Optional vertical reference line (e.g. the world average) and its
        label — instant context for "how far above normal".
    vmax
        Upper bound for the color ramp. Pass the same ``vmax`` to several
        charts so a bar of a given darkness means the same emissions in each.
        Defaults to this chart's maximum.
    unit
        Unit string appended to the reference label / used in labels.
    value_fmt
        Format string for the value labels.
    title, subtitle, note
        Takeaway title, units/what-am-I-looking-at subtitle, and a source note.
    ascending
        Sort direction; default puts the largest bar on top.
    ax, figsize
        Optional target Axes and figure size (height auto-scales with bars).

    Returns
    -------
    matplotlib.figure.Figure
    """
    apply_theme()

    data = df[[category, value] + ([compare] if compare else [])].dropna(subset=[value])
    data = data.sort_values(value, ascending=ascending).reset_index(drop=True)
    labels = data[category].tolist()
    values = data[value].tolist()
    n = len(values)
    if n == 0:
        raise ValueError("no rows to plot after dropping missing values")

    top = vmax if vmax is not None else max(values)

    owns_fig = ax is None
    if owns_fig:
        if figsize is None:
            figsize = (7.6, 0.52 * n + 1.7)
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    # bars top-to-bottom (largest at top when ascending=False)
    y = list(range(n))[::-1]
    for yi, val in zip(y, values):
        ax.barh(yi, val, height=0.68, color=smog_color(val, top), zorder=3)

    xmax = max(values + ([reference] if reference else []))
    ax.set_xlim(0, xmax * 1.16)  # head-room for end labels

    # direct value labels (+ optional change tag) at each bar end
    for yi, (val, row) in zip(y, zip(values, data.itertuples(index=False))):
        label = value_fmt.format(val)
        ax.annotate(label, xy=(val, yi), xytext=(6, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=11, fontweight="bold",
                    color="#0b0b0b")
        if compare:
            prev = getattr(row, compare) if hasattr(row, compare) else None
            if prev:
                pct = (val - prev) / prev * 100
                up = pct >= 0
                tag = f"  {_UP if up else _DOWN} {abs(pct):.0f}%"
                # up = more emissions (bad) = warm; down = good = green
                ax.annotate(tag, xy=(val, yi), xytext=(6 + 34, 0),
                            textcoords="offset points", va="center", ha="left",
                            fontsize=9.5, fontweight="bold",
                            color="#c0392b" if up else "#0a7d33")

    # optional reference line for context, labelled at the baseline
    if reference is not None:
        ax.axvline(reference, color="#52514e", linestyle=(0, (4, 3)),
                   linewidth=1.2, zorder=2)
        rlab = reference_label or "reference"
        val_txt = f"{value_fmt.format(reference)}{(' ' + unit) if unit else ''}"
        ax.annotate(f"{rlab} ({val_txt})", xy=(reference, -0.75),
                    xytext=(4, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=9.5, style="italic",
                    color="#52514e")

    # category labels; strip every non-data line (checklist: mute the lines)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xticks([])
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    ax.grid(False)
    ax.tick_params(length=0)
    # headroom above the top bar for the subtitle, a little below for the ref label
    ax.set_ylim(-1.1, n - 1 + 0.9)

    # titles: takeaway on top, quiet subtitle beneath, source note at the foot
    if title:
        ax.set_title(title, loc="left", fontsize=15, fontweight="bold", pad=24)
    if subtitle:
        ax.annotate(subtitle, xy=(0, 1.0), xycoords="axes fraction",
                    xytext=(0, 8), textcoords="offset points",
                    ha="left", va="bottom", fontsize=11, color="#52514e")
    if note:
        ax.annotate(note, xy=(0, 0), xycoords="axes fraction",
                    xytext=(0, -26), textcoords="offset points",
                    ha="left", va="top", fontsize=8.5, color="#898781")

    if owns_fig:
        fig.tight_layout()
    return fig


def stacked_bar(
    df,
    category: str,
    segments: list[str],
    *,
    colors=None,
    ascending: bool = False,
    unit: str = "",
    value_fmt: str = "{:.0f}",
    seg_label_min: float = 0.08,
    title: str | None = None,
    subtitle: str | None = None,
    note: str | None = None,
    legend: bool = True,
    ax=None,
    figsize: tuple[float, float] | None = None,
):
    """Draw a ranked, stacked horizontal bar chart from a pandas DataFrame.

    Each row is one category (e.g. a country); ``segments`` are the columns
    that stack into its total. Rows are ordered by total, the total is labelled
    at the bar end, and wide-enough segments are labelled in place — the same
    idea as the Our World in Data "by source" charts.

    Parameters
    ----------
    df
        A pandas DataFrame, one row per category.
    category
        Column holding the row label per bar.
    segments
        Columns to stack, left-to-right. Missing values count as zero.
    colors
        ``None`` assigns the categorical palette in order (segments are
        categories — identity, not magnitude), or a dict of overrides.
    ascending
        Sort direction by total; default puts the largest total on top.
    unit, value_fmt
        Unit suffix and number format for the labels.
    seg_label_min
        Only label a segment in place if it is at least this fraction of the
        largest row total (keeps small slivers uncluttered).
    title, subtitle, note
        Takeaway title, quiet subtitle, and source note.
    legend
        Draw a segment legend above the plot (default True).
    ax, figsize
        Optional target Axes and figure size (height auto-scales with rows).

    Returns
    -------
    matplotlib.figure.Figure
    """
    apply_theme()

    data = df[[category] + segments].copy()
    for s in segments:
        data[s] = data[s].fillna(0.0)
    data["_total"] = data[segments].sum(axis=1)
    data = data.sort_values("_total", ascending=ascending).reset_index(drop=True)
    n = len(data)
    if n == 0:
        raise ValueError("no rows to plot")

    overrides = dict(colors) if isinstance(colors, dict) else {}
    seg_colors = {s: overrides.get(s, series_color(i)) for i, s in enumerate(segments)}

    owns_fig = ax is None
    if owns_fig:
        if figsize is None:
            figsize = (9.0, 0.55 * n + 2.0)
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    y = list(range(n))[::-1]
    max_total = float(data["_total"].max())
    label_floor = max_total * seg_label_min

    for yi, (_, row) in zip(y, data.iterrows()):
        left = 0.0
        for s in segments:
            w = float(row[s])
            if w <= 0:
                continue
            color = seg_colors[s]
            ax.barh(yi, w, left=left, height=0.7, color=color, zorder=3,
                    edgecolor=_SURFACE, linewidth=1.0)
            if w >= label_floor:  # label only segments wide enough to fit
                ax.annotate(value_fmt.format(w), xy=(left + w / 2, yi),
                            ha="center", va="center", fontsize=9.5,
                            fontweight="bold", color=_readable_ink(color), zorder=4)
            left += w
        # total at the bar end
        ax.annotate(f"{value_fmt.format(left)}{(' ' + unit) if unit else ''}",
                    xy=(left, yi), xytext=(6, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=11, fontweight="bold",
                    color="#0b0b0b")

    ax.set_xlim(0, max_total * 1.16)
    ax.set_ylim(-0.8, n - 1 + (1.4 if legend else 0.7))
    ax.set_yticks(y)
    ax.set_yticklabels(data[category].tolist(), fontsize=11)
    ax.set_xticks([])
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    ax.grid(False)
    ax.tick_params(length=0)

    if legend:
        handles = [Patch(facecolor=seg_colors[s], label=s) for s in segments]
        ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, 1.0),
                  ncol=min(len(segments), 6), frameon=False, fontsize=9.5,
                  handlelength=1.1, columnspacing=1.4, borderaxespad=0)

    if title:
        ax.set_title(title, loc="left", fontsize=15, fontweight="bold", pad=44)
    if subtitle:
        ax.annotate(subtitle, xy=(0, 1.0), xycoords="axes fraction",
                    xytext=(0, 26), textcoords="offset points", ha="left",
                    va="bottom", fontsize=11, color="#52514e")
    if note:
        ax.annotate(note, xy=(0, 0), xycoords="axes fraction", xytext=(0, -26),
                    textcoords="offset points", ha="left", va="top",
                    fontsize=8.5, color="#898781")

    if owns_fig:
        fig.tight_layout()
    return fig
