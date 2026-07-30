"""viz_lib — a small, consistent plotting library.

Every plot function follows the same contract:

* takes tidy data plus role keywords (``x``, ``y``, ``series`` ...),
* accepts an optional ``ax`` so plots compose into larger figures,
* returns the matplotlib object it drew on (``Axes`` or ``Figure``),
* is styled by a single shared theme so all plots share one identity.

The first plot shipped is :func:`split_panel_line`, which draws one metric
across several series split into two (or more) panels — the honest answer to
"some series are 30x larger than others" without resorting to a log axis.
"""

from .theme import PALETTE, SMOG, apply_theme, series_color, smog_color
from .line import split_panel_line
from .bar import ranked_bar
from .area import stacked_area
from . import datasets
from .datasets import load as load_dataset

__all__ = [
    "PALETTE",
    "SMOG",
    "apply_theme",
    "series_color",
    "smog_color",
    "split_panel_line",
    "ranked_bar",
    "stacked_area",
    "datasets",
    "load_dataset",
]
