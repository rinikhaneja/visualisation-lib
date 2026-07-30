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

from .theme import apply_theme, smog_color

_UP, _DOWN = "▲", "▼"  # ▲ ▼


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
